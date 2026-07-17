import json
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from hebrew_names import HEBREW_NAMES

INDICATORS = [
    ("net_migration", "SM.POP.NETM", "wb_SM_POP_NETM.json",
     "מאזן הגירה (מספר מהגרים נטו, ל-5 שנים)"),
    ("life_expectancy", "SP.DYN.LE00.IN", "wb_SP_DYN_LE00_IN.json",
     "תוחלת חיים בלידה (שנים)"),
    ("literacy_rate", "SE.ADT.LITR.ZS", "wb_SE_ADT_LITR_ZS.json",
     "אחוז יודעי קרוא וכתוב (גילאי 15+)"),
    ("birth_rate", "SP.DYN.CBRT.IN", "wb_SP_DYN_CBRT_IN.json",
     "שיעור ילודה (ל-1,000 נפש)"),
    ("death_rate", "SP.DYN.CDRT.IN", "wb_SP_DYN_CDRT_IN.json",
     "שיעור תמותה (ל-1,000 נפש)"),
    ("urban_pct", "SP.URB.TOTL.IN.ZS", "wb_SP_URB_TOTL_IN_ZS.json",
     "אחוז עירוניות (% מהאוכלוסייה)"),
]

# 1. load country metadata, keep only real countries (not aggregates)
meta = json.load(open("countries_meta.json", encoding="utf-8"))[1]
real_countries = {}
for r in meta:
    if r["region"]["value"] != "Aggregates":
        real_countries[r["id"]] = r["name"]

print("real countries:", len(real_countries))

# 2. load each indicator's data -> iso3 -> {value, date}
indicator_data = {}
for key, code, fname, label in INDICATORS:
    d = json.load(open(fname, encoding="utf-8"))[1]
    vals = {}
    for rec in d:
        iso3 = rec.get("countryiso3code")
        if not iso3 or iso3 not in real_countries:
            continue
        if rec.get("value") is None:
            continue
        vals[iso3] = {"value": rec["value"], "year": rec["date"]}
    indicator_data[key] = vals
    print(key, "-> matched countries:", len(vals))

# 3. load boundaries geojson
geo = json.load(open("countries.geojson", encoding="utf-8"))
print("geo features:", len(geo["features"]))

features_by_iso3 = {}
NAME_ISO3_OVERRIDES = {
    "France": "FRA",
    "Norway": "NOR",
    "Kosovo": "XKX",
}
for f in geo["features"]:
    iso3 = f["properties"].get("ISO3166-1-Alpha-3")
    name = f["properties"].get("name")
    if iso3 == "-99" and name in NAME_ISO3_OVERRIDES:
        iso3 = NAME_ISO3_OVERRIDES[name]
    if iso3 and iso3 != "-99":
        features_by_iso3[iso3] = f

# 4. merge Palestine geometry into Israel
isr_feat = features_by_iso3.get("ISR")
pse_feat = features_by_iso3.get("PSE")
if isr_feat and pse_feat:
    isr_geom = shape(isr_feat["geometry"])
    pse_geom = shape(pse_feat["geometry"])
    merged = unary_union([isr_geom, pse_geom])
    isr_feat["geometry"] = mapping(merged)
    print("Merged Palestine geometry into Israel. New geom type:", merged.geom_type)

# 5. build final feature list: only real countries, skip PSE (merged away), skip unmatched iso3
final_features = []
skipped_no_iso3 = []
matched_iso3 = set()

for iso3, name in real_countries.items():
    feat = features_by_iso3.get(iso3)
    if iso3 == "PSE":
        continue  # merged into Israel, not shown separately
    if not feat:
        continue
    matched_iso3.add(iso3)
    props = {
        "name": HEBREW_NAMES.get(iso3, name),
        "name_en": name,
        "iso3": iso3,
    }
    for key, code, fname, label in INDICATORS:
        entry = indicator_data[key].get(iso3)
        props[key] = entry["value"] if entry else None
        props[key + "_year"] = entry["year"] if entry else None
    new_feat = {
        "type": "Feature",
        "properties": props,
        "geometry": feat["geometry"],
    }
    final_features.append(new_feat)

print("final countries included:", len(final_features))
missing_geo = set(real_countries) - matched_iso3 - {"PSE"}
print("countries with no boundary geometry (excluded):", sorted(missing_geo))

# 6. simplify geometry (Douglas-Peucker) to cut vertex count for smooth web rendering,
# then round coordinates to reduce file size (~11m precision)
SIMPLIFY_TOLERANCE_DEG = 0.02  # ~ 2.2 km at the equator

def round_coords(coords, ndigits=4):
    if isinstance(coords[0], (int, float)):
        return [round(c, ndigits) for c in coords]
    return [round_coords(c, ndigits) for c in coords]

total_pts_before = 0
total_pts_after = 0
for f in final_features:
    geom = shape(f["geometry"])
    total_pts_before += sum(len(p.exterior.coords) for p in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]))
    simplified = geom.simplify(SIMPLIFY_TOLERANCE_DEG, preserve_topology=True)
    if simplified.is_empty:
        simplified = geom  # keep original if simplification collapsed the shape
    total_pts_after += sum(len(p.exterior.coords) for p in (simplified.geoms if simplified.geom_type == "MultiPolygon" else [simplified]))
    f["geometry"] = mapping(simplified)
    f["geometry"]["coordinates"] = round_coords(f["geometry"]["coordinates"])

print(f"vertex count: {total_pts_before} -> {total_pts_after}")

final_geo = {"type": "FeatureCollection", "features": final_features}

import os
os.makedirs("../data", exist_ok=True)

with open("../data/world_data.geojson", "w", encoding="utf-8") as fh:
    json.dump(final_geo, fh, ensure_ascii=False, separators=(",", ":"))

print("output size bytes:", os.path.getsize("../data/world_data.geojson"))

# 7. compute stats per indicator for legend breaks (quantiles over available values)
stats = {}
for key, code, fname, label in INDICATORS:
    values = sorted(v for v in (f["properties"][key] for f in final_features) if v is not None)
    n = len(values)
    if n == 0:
        stats[key] = None
        continue
    def q(p):
        idx = min(n - 1, max(0, int(round(p * (n - 1)))))
        return values[idx]
    stats[key] = {
        "min": values[0],
        "max": values[-1],
        "q20": q(0.2),
        "q40": q(0.4),
        "q60": q(0.6),
        "q80": q(0.8),
        "count_with_data": n,
        "count_total": len(final_features),
        "indicator_code": code,
        "label_he": label,
    }

with open("../data/indicator_stats.json", "w", encoding="utf-8") as fh:
    json.dump(stats, fh, ensure_ascii=False, indent=2)

for k, v in stats.items():
    print(k, v)
