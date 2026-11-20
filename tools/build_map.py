#!/usr/bin/env python3
"""Convert a Geofabrik GeoPackage (OpenStreetMap, ODbL) into a compact, spatially indexed
map database the app can draw offline.

  python3 tools/build_map.py derived/geo/socal.gpkg derived/geo/map.sqlite

Input is a copy extracted from any Geofabrik <region>-latest-free.gpkg.zip (a US state or a
region outside it); the original archive is only read. The `source`, `data_as_of` and `bounds`
rows in `meta` are taken from the input file, not hard-coded. Output tables:
  feat(id, layer, cls, name, minz, geom)   geom = packed int32 lon/lat * 1e6 (see pack())
  feat_idx (R*Tree on bbox)
  poi(id, cls, name, lon, lat)             help-relevant points (hospitals, pharmacies, water...)
  meta(key, value)
"""
import math, os, re, sqlite3, struct, sys, time, zipfile
from array import array
from pathlib import Path

SRC, DST = sys.argv[1], sys.argv[2]
Q = 1e6

ROAD_Z = {'motorway': 5, 'trunk': 6, 'motorway_link': 10, 'trunk_link': 10, 'primary': 8, 'primary_link': 12,
          'secondary': 10, 'secondary_link': 13, 'tertiary': 11, 'tertiary_link': 13, 'residential': 13,
          'unclassified': 13, 'living_street': 14, 'pedestrian': 14, 'busway': 14, 'service': 15,
          'track': 13, 'track_grade1': 13, 'track_grade2': 13, 'track_grade3': 13, 'track_grade4': 13, 'track_grade5': 13,
          'footway': 15, 'path': 14, 'cycleway': 14, 'steps': 16, 'bridleway': 14, 'unknown': 15}
LANDUSE_KEEP = {'park': 'park', 'forest': 'green', 'grass': 'green', 'meadow': 'green', 'scrub': 'green', 'heath': 'green',
                'recreation_ground': 'park', 'cemetery': 'park', 'allotments': 'farm', 'farmland': 'farm',
                'orchard': 'farm', 'vineyard': 'farm', 'farmyard': 'farm', 'residential': 'res', 'commercial': 'com',
                'retail': 'com', 'industrial': 'ind', 'military': 'ind', 'quarry': 'ind', 'landfill': 'ind'}
PLACE_Z = {'county': 7, 'city': 6, 'town': 9, 'suburb': 12, 'village': 11, 'hamlet': 14, 'locality': 14, 'island': 11,
           'farm': 15, 'region': 5}
# Points people look for when services fail. Names shown in the app come from the app, not from here.
POI_KEEP = {'hospital', 'clinic', 'doctors', 'pharmacy', 'chemist', 'dentist', 'veterinary', 'fire_station', 'police',
            'drinking_water', 'water_tower', 'water_works', 'fountain', 'toilet', 'shelter', 'community_centre',
            'town_hall', 'school', 'library', 'supermarket', 'convenience', 'doityourself', 'hardware', 'garden_centre',
            'post_office', 'camp_site', 'wastewater_plant', 'comms_tower', 'spring', 'park', 'courthouse', 'embassy',
            'nursing_home', 'kindergarten', 'college', 'university', 'bicycle_shop', 'car_repair', 'fuel', 'beach'}


def wkb_parts(b, o):
    """Return (list of parts as flat [x,y,...] lists, offset). Polygons yield their rings as parts."""
    le = b[o] == 1
    e = '<' if le else '>'
    t = struct.unpack_from(e + 'I', b, o + 1)[0] % 1000
    o += 5
    if t == 1:
        x, y = struct.unpack_from(e + 'dd', b, o)
        return [[x, y]], o + 16
    if t == 2:
        n = struct.unpack_from(e + 'I', b, o)[0]
        return [list(struct.unpack_from(e + '%dd' % (2 * n), b, o + 4))], o + 4 + 16 * n
    if t == 3:
        nr = struct.unpack_from(e + 'I', b, o)[0]
        o += 4
        parts = []
        for _ in range(nr):
            n = struct.unpack_from(e + 'I', b, o)[0]
            parts.append(list(struct.unpack_from(e + '%dd' % (2 * n), b, o + 4)))
            o += 4 + 16 * n
        return parts, o
    if t in (4, 5, 6, 7):
        n = struct.unpack_from(e + 'I', b, o)[0]
        o += 4
        parts = []
        for _ in range(n):
            p, o = wkb_parts(b, o)
            parts.extend(p)
        return parts, o
    raise ValueError('geometry type %d' % t)


def gpkg_parts(g):
    flags = g[3]
    env = (flags >> 1) & 7
    off = 8 + {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[env]
    return wkb_parts(g, off)[0]


def simplify(flat, tol):
    """Drop points closer than tol (degrees) to the previous kept point; keeps endpoints."""
    if len(flat) <= 4 or tol <= 0:
        return flat
    out = [flat[0], flat[1]]
    px, py = flat[0], flat[1]
    for i in range(2, len(flat) - 2, 2):
        x, y = flat[i], flat[i + 1]
        if abs(x - px) > tol or abs(y - py) > tol:
            out += [x, y]
            px, py = x, y
    out += [flat[-2], flat[-1]]
    return out


def pack(parts):
    """int32 array: nparts, then for each part npts followed by quantized x,y deltas."""
    a = array('i', [len(parts)])
    for p in parts:
        n = len(p) // 2
        a.append(n)
        lx = ly = 0
        for i in range(n):
            x, y = int(round(p[2 * i] * Q)), int(round(p[2 * i + 1] * Q))
            a.append(x - lx); a.append(y - ly)
            lx, ly = x, y
    return a.tobytes()


def bbox(parts):
    xs = [v for p in parts for v in p[0::2]]
    ys = [v for p in parts for v in p[1::2]]
    return min(xs), max(xs), min(ys), max(ys)


def area_z(minx, maxx, miny, maxy, base):
    """Small polygons only appear when zoomed in."""
    size = max(maxx - minx, maxy - miny)
    if size <= 0:
        return 17
    z = int(math.log2(360 / size)) - 4  # visible when ~1/16 of the screen-ish
    return max(base, min(16, z))


def source_facts(path):
    """The archive and the OpenStreetMap data date this GeoPackage came from.

    Geofabrik's README inside the zip states the data date; the GeoPackage's own
    gpkg_contents.last_change is when the extract was built, which is close but not
    the same fact. The file's mtime is the last fallback.
    """
    p = Path(path)
    zip_path = p.with_name(p.stem + '-latest-free.gpkg.zip')
    archive = zip_path.name if zip_path.exists() else p.name
    date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(p)))
    stated = None
    try:
        with zipfile.ZipFile(zip_path) as z:
            readme = z.read('README').decode('utf-8', 'replace')
        m = re.search(r'data as of (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', readme)
        if m:
            stated = m.group(1)
    except (OSError, KeyError, zipfile.BadZipFile):
        pass
    if stated:
        return archive, stated
    try:
        db = sqlite3.connect(path)
        row = db.execute('SELECT MAX(last_change) FROM gpkg_contents').fetchone()
        db.close()
        if row and row[0]:
            stamp = str(row[0]).strip().replace(' ', 'T').rstrip('Z')
            date = stamp[:19] + 'Z'
    except sqlite3.Error:
        pass
    return archive, date


def outer_box(world, step=100):
    """The bounds rounded outwards to two decimals, so no feature falls outside them."""
    return (math.floor(world[0] * step) / step, math.floor(world[1] * step) / step,
            math.ceil(world[2] * step) / step, math.ceil(world[3] * step) / step)


def main():
    t0 = time.time()
    src = sqlite3.connect(SRC)
    source_archive, data_date = source_facts(SRC)
    world = [None, None, None, None]  # min lon, min lat, max lon, max lat over everything added
    dst = sqlite3.connect(DST)
    dst.executescript('''PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;
      DROP TABLE IF EXISTS feat; DROP TABLE IF EXISTS feat_idx; DROP TABLE IF EXISTS poi; DROP TABLE IF EXISTS meta;
      CREATE TABLE feat(id INTEGER PRIMARY KEY, layer TEXT, cls TEXT, name TEXT, minz INTEGER, geom BLOB);
      CREATE VIRTUAL TABLE feat_idx USING rtree(id, minx, maxx, miny, maxy, minz, maxz);
      CREATE TABLE poi(id INTEGER PRIMARY KEY, cls TEXT, name TEXT, lon REAL, lat REAL);
      CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);''')
    fid = [0]

    def add(layer, cls, name, minz, parts):
        if not parts:
            return
        fid[0] += 1
        bx = bbox(parts)
        if world[0] is None:
            world[:] = [bx[0], bx[2], bx[1], bx[3]]
        else:
            world[0] = min(world[0], bx[0]); world[1] = min(world[1], bx[2])
            world[2] = max(world[2], bx[1]); world[3] = max(world[3], bx[3])
        dst.execute('INSERT INTO feat VALUES (?,?,?,?,?,?)', (fid[0], layer, cls, name, minz, pack(parts)))
        dst.execute('INSERT INTO feat_idx VALUES (?,?,?,?,?,?,?)', (fid[0], *bx, minz, 30))

    def each(table, cols='fclass,name'):
        for row in src.execute(f'SELECT geom,{cols} FROM {table}'):
            if row[0] is None:
                continue
            try:
                yield gpkg_parts(row[0]), row[1:]
            except Exception:
                continue

    # Water bodies
    for parts, (cls, name) in each('gis_osm_water_a_free'):
        layer = 'wet' if cls.startswith('wetland') else 'water'
        b = bbox(parts)
        add(layer, cls, name, area_z(*b, 7), [simplify(p, 0.00001) for p in parts])
    print('water', fid[0], round(time.time() - t0), flush=True)
    for parts, (cls, name) in each('gis_osm_natural_a_free'):
        if cls == 'beach':
            add('beach', cls, name, area_z(*bbox(parts), 10), parts)
    for parts, (cls, name) in each('gis_osm_landuse_a_free'):
        k = LANDUSE_KEEP.get(cls)
        if k:
            add('land', k, name, area_z(*bbox(parts), 9), [simplify(p, 0.00001) for p in parts])
    for parts, (cls,) in each('gis_osm_protected_areas_a_free', 'fclass'):
        add('land', 'park', None, area_z(*bbox(parts), 8), [simplify(p, 0.00002) for p in parts])
    print('land', fid[0], round(time.time() - t0), flush=True)
    for parts, (cls, name) in each('gis_osm_waterways_free'):
        add('waterway', cls, name, 10 if cls == 'river' else 13, parts)
    for parts, (cls, name) in each('gis_osm_railways_free'):
        add('rail', cls, name, 10 if cls == 'rail' else 13, parts)
    print('lines', fid[0], round(time.time() - t0), flush=True)
    for parts, (cls, name, ref) in each('gis_osm_roads_free', 'fclass,name,ref'):
        label = name or ref
        add('road', cls, label, ROAD_Z.get(cls, 15), parts)
    print('roads', fid[0], round(time.time() - t0), flush=True)
    dst.commit()
    for parts, (cls, name) in each('gis_osm_buildings_a_free'):
        add('bldg', cls or '', None, 15, [simplify(parts[0], 0.000002)])
    print('buildings', fid[0], round(time.time() - t0), flush=True)
    dst.commit()
    for parts, (cls, pop, name) in each('gis_osm_places_free', 'fclass,population,name'):
        if name:
            z = PLACE_Z.get(cls, 14)
            if cls in ('city', 'town') and pop and int(pop) > 300000:
                z = 5
            add('place', cls, name, z, parts)
    pid = 0
    for table in ('gis_osm_pois_free', 'gis_osm_pois_a_free', 'gis_osm_natural_free', 'gis_osm_natural_a_free'):
        for parts, (cls, name) in each(table):
            if cls not in POI_KEEP:
                continue
            if table == 'gis_osm_natural_free' and cls not in ('spring',):
                continue
            minx, maxx, miny, maxy = bbox(parts)
            if world[0] is None:
                world[:] = [minx, miny, maxx, maxy]
            else:
                world[0] = min(world[0], minx); world[1] = min(world[1], miny)
                world[2] = max(world[2], maxx); world[3] = max(world[3], maxy)
            pid += 1
            dst.execute('INSERT INTO poi VALUES (?,?,?,?,?)', (pid, cls, name, (minx + maxx) / 2, (miny + maxy) / 2))
    dst.execute('CREATE INDEX poi_cls ON poi(cls, lon, lat)')
    dst.executemany('INSERT INTO meta VALUES (?,?)', [
        ('source', f'OpenStreetMap contributors, via Geofabrik {source_archive} (ODbL 1.0)'),
        ('data_as_of', data_date),
        ('bounds', '%.2f,%.2f,%.2f,%.2f' % outer_box(world) if world[0] is not None else ''),
        ('built', time.strftime('%Y-%m-%dT%H:%M:%S')),
    ])
    dst.commit()
    print('done features', fid[0], 'pois', pid, round(time.time() - t0), 's', flush=True)


main()
