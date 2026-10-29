"""data.json + posters (clean frames, 480 px) + pack covers (960 px) for the presets-1000 site."""
import json, os, glob
from PIL import Image
LIB = "/Users/nurbek.s/Documents/Claude/2026-10-28/motion-library/lib1000"; OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{OUT}/posters", exist_ok=True); os.makedirs(f"{OUT}/packs", exist_ok=True)
FORCE = os.environ.get("FORCE") == "1"  # re-make posters and pack covers (after re-rendered covers)
packs = json.load(open(f"{LIB}/packs_index.json")); full = {p["pack_id"]: p for p in json.load(open(f"{LIB}/packs.json"))}
cats = []; seen = {}
data = {"packs": [], "categories": []}
for pk in packs:
    vs = []
    for i in pk["presets"]:
        m = json.load(open(f"{LIB}/manifests/{i}.json"))
        d = glob.glob(f"{LIB}/presets/*/{i}")[0]
        po = f"posters/{i}.jpg"
        if FORCE or not os.path.exists(f"{OUT}/{po}"):
            im = Image.open(f"{d}/frame.jpg").convert("RGB"); s = 480 / min(im.size); im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).save(f"{OUT}/{po}", quality=80)
        slots = [s["key"] for s in m["slots"] if s["key"].startswith("copy.")]
        vs.append({"id": i, "code": m["code"], "aspect": m["format"]["aspect"], "palette": json.load(open(f"{d}/params.json"))["palette_name"],
                   "poster": po, "video": f"media/{i}.mp4", "slots": slots})
    src = f"{LIB}/pack_covers/{pk['pack_id']} {pk['word']} {pk['title']}.jpg"; pc = f"packs/{pk['pack_id']}.jpg"
    if FORCE or not os.path.exists(f"{OUT}/{pc}"): Image.open(src).convert("RGB").resize((960, 540), Image.LANCZOS).save(f"{OUT}/{pc}", quality=82)
    m0 = json.load(open(f"{LIB}/manifests/{pk['presets'][0]}.json"))
    cat = m0["category"]
    if cat["slug"] not in seen:
        seen[cat["slug"]] = 1; data["categories"].append({"slug": cat["slug"], "en": cat["en"].split(" (")[0], "ru": cat["ru"], "packs": 0, "presets": 0})
    c = next(x for x in data["categories"] if x["slug"] == cat["slug"]); c["packs"] += 1; c["presets"] += len(vs)
    data["packs"].append({"id": pk["pack_id"], "word": pk["word"], "title": pk["title"], "category": cat["slug"], "what": pk["what_it_does"],
                          "cover": pc, "variants": vs})
json.dump(data, open(f"{OUT}/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(data["packs"]), "packs", sum(len(p["variants"]) for p in data["packs"]), "presets", len(data["categories"]), "categories")
