"""Figure 2 from the relation export with a reproducible selection rule.

Rule: every unordered endpoint pair (self-loops excluded) with at least MIN_RECORDS relation records in
data/relations.csv; the nodes are the endpoints of those pairs. Names are normalized as in Section 3.5.1
(trim, case-fold, collapse internal whitespace). Each edge is drawn with its most frequent relation type;
causal and description edges point in the majority direction of the records of that type. Edge width and
label give the number of relation records for the pair.
Usage: python figure2.py path/to/relations.csv figure2.png
"""
import re, sys
from collections import Counter, defaultdict
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

MIN_RECORDS = 7
plt.rcParams["font.family"] = "Liberation Sans"
src, out = sys.argv[1], sys.argv[2]
norm = lambda s: re.sub(r"\s+", " ", str(s).strip()).casefold()

r = pd.read_csv(src, dtype=str, keep_default_na=False)
pair_n, pair_types, dir_n = Counter(), defaultdict(Counter), Counter()
for s, t, rel in zip(r.source_node.map(norm), r.target_node.map(norm), r.relation):
    if s == t: continue
    k = tuple(sorted((s, t)))
    pair_n[k] += 1; pair_types[k][rel] += 1; dir_n[(s, t, rel)] += 1
sel = [(k, n) for k, n in pair_n.most_common() if n >= MIN_RECORDS]
nodes = sorted({x for k, _ in sel for x in k})
print(f"{len(sel)} pairs with >= {MIN_RECORDS} records; {len(nodes)} nodes:", nodes)

# hand-placed layout for the selected nodes (positions only; content is data-driven)
POS = {
    "river": ("River", -2.55, 2.45),
    "cremations": ("Cremations", -0.35, 2.45),
    "ghats": ("Ghats", 1.35, 3.55),
    "guide": ("Guide", 1.55, 1.75),
    "cremation": ("Cremation", -2.75, 0.85),
    "bagmati river": ("Bagmati River", 0.0, 0.0),
    "cremation ceremony": ("Cremation ceremony", 3.05, 0.55),
    "sense of mortality": ("Sense of mortality", 4.45, 2.3),
    "non-hindu entry ban": ("Non-Hindu entry ban", 2.35, -1.75),
    "main temple": ("Main temple", -0.6, -2.55),
    "entrance fee": ("Entrance fee", 1.35, -3.6),
    "entry fee for foreigners": ("Entry fee for foreigners", 4.05, -2.95),
}
missing = set(nodes) - set(POS)
if missing: raise SystemExit(f"no position for {missing}")

edges = []
for (a, b), n in sel:
    rel = pair_types[(a, b)].most_common(1)[0][0]
    if rel in ("causal", "description") and dir_n[(b, a, rel)] > dir_n[(a, b, rel)]:
        a, b = b, a
    edges.append((a, b, rel, n))
print("edges:", [(a, b, rel, n) for a, b, rel, n in edges])

STY = {  # greyscale-safe: line style carries the type, arrows carry direction
    "co_occurrence": dict(color="#8a8a8a", ls="-", arrow=False, label="Co-occurrence (symmetric)"),
    "contrast": dict(color="#1a1a1a", ls=(0, (5, 2.2)), arrow=False, label="Contrast (symmetric)"),
    "causal": dict(color="#1a1a1a", ls="-", arrow=True, label="Causal (directed)"),
    "description": dict(color="#1a1a1a", ls=(0, (0.9, 1.5)), arrow=True, label="Description (directed)"),
}
W, H = 6.3, 5.0
fig = plt.figure(figsize=(W, H), dpi=600)
ax = fig.add_axes([0.01, 0.12, 0.98, 0.87]); ax.set_xlim(-3.75, 5.75); ax.set_ylim(-4.05, 4.0); ax.axis("off")
ax.set_aspect("equal"); ax.apply_aspect(); fig.canvas.draw()
FS = 9.2
rend = fig.canvas.get_renderer()
half = {}
for nid in nodes:
    lab, x, y = POS[nid]
    t = ax.text(x, y, lab, ha="center", va="center", fontsize=FS, color="#111111", zorder=4)
    bb = t.get_window_extent(rend).transformed(ax.transData.inverted())
    half[nid] = ((bb.x1 - bb.x0) / 2 + 0.16, (bb.y1 - bb.y0) / 2 + 0.11)
    hw, hh = half[nid]
    ax.add_patch(FancyBboxPatch((x - hw, y - hh), 2 * hw, 2 * hh, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor="white", edgecolor="#262626", linewidth=0.8, zorder=3))

def border_point(nid, dx, dy):
    hw, hh = half[nid]
    sx = hw / abs(dx) if dx else float("inf"); sy = hh / abs(dy) if dy else float("inf")
    s = min(sx, sy); x, y = POS[nid][1], POS[nid][2]
    return x + dx * s, y + dy * s

for a, b, rel, n in edges:
    xa, ya = POS[a][1:]; xb, yb = POS[b][1:]
    dx, dy = xb - xa, yb - ya
    p0 = border_point(a, dx, dy); p1 = border_point(b, -dx, -dy)
    st = STY.get(rel, STY["co_occurrence"]); lw = 0.6 + 0.11 * n
    if st["arrow"]:
        L = ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
        f = max(0.0, 1 - 0.32 / L)
        pm = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
        ax.plot([p0[0], pm[0]], [p0[1], pm[1]], color=st["color"], linewidth=lw, linestyle=st["ls"],
                solid_capstyle="butt", dash_capstyle="round", zorder=2)
        ax.add_patch(FancyArrowPatch(pm, p1, arrowstyle="-|>", mutation_scale=8 + 0.15 * n, linewidth=lw,
                                     color=st["color"], linestyle="-", shrinkA=0, shrinkB=1.5, zorder=2))
    else:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=st["color"], linewidth=lw, linestyle=st["ls"],
                solid_capstyle="butt", dash_capstyle="butt", zorder=2)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    ax.text(mx, my, str(n), ha="center", va="center", fontsize=8.2, color="#111111", zorder=5,
            bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="none"))

used = [k for k in ["co_occurrence", "contrast", "causal", "description"] if any(e[2] == k for e in edges)]
handles = [Line2D([0, 1], [0, 0], color=STY[k]["color"], linestyle=STY[k]["ls"], linewidth=1.6, dash_capstyle="round",
                  marker=">" if STY[k]["arrow"] else None, markersize=5, markevery=[1], label=STY[k]["label"])
           for k in used]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8, handlelength=3.2,
           columnspacing=2.2, bbox_to_anchor=(0.5, 0.005))
fig.savefig(out, dpi=600, facecolor="white")
if out.endswith(".png"):
    fig.savefig(out[:-4] + ".tif", dpi=600, facecolor="white", pil_kwargs={"compression": "tiff_lzw"})
print("saved", out)
