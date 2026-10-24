"""Recompute the node and relation-graph counts reported in Table 6 of the paper.
Usage: python graph_counts.py path/to/data/   (folder containing entity_mentions.csv and relations.csv)
Normalization: trim, case-fold, collapse internal whitespace (Section 3.5.1).
"""
import re, sys, pandas as pd, networkx as nx
base = sys.argv[1]
def norm(s): return re.sub(r"\s+", " ", str(s).strip()).casefold()
e = pd.read_csv(base+"entity_mentions.csv", dtype=str, keep_default_na=False)
r = pd.read_csv(base+"relations.csv", dtype=str, keep_default_na=False)
ent = set(e.entity_name.map(norm)) - {""}
r["s"] = r.source_node.map(norm); r["t"] = r.target_node.map(norm)
endpoints = set(r.s) | set(r.t)
print("entity-name nodes:", len(ent))
print("relation endpoint nodes:", len(endpoints))
print("entity names not endpoints:", len(ent - endpoints))
print("endpoints not in entity names:", len(endpoints - ent))
print("merged inventory:", len(ent | endpoints))
schema = {"co_occurrence","causal","description","contrast"}
sym = {"co_occurrence","contrast"}
def key(row):
    s,t,rel = row.s,row.t,row.relation
    if rel in sym and t < s: s,t = t,s
    return (s,t,rel, rel in schema)
groups = r.apply(key, axis=1)
g = pd.Series(list(groups)).value_counts()
print("typed edge groups:", len(g), " in-schema:", sum(1 for k in g.index if k[3]), " out-of-schema:", sum(1 for k in g.index if not k[3]))
print("self-loop groups:", sum(1 for k in g.index if k[0]==k[1]))
print("unique ordered pairs ignoring label:", len(set(zip(r.s,r.t))))
def und(keys):
    G = nx.Graph()
    for (s,t,rel,ok) in keys:
        G.add_node(s); G.add_node(t)
        if s!=t: G.add_edge(s,t)
    return G
G = und(g.index)
print("undirected: nodes", G.number_of_nodes(), "edges", G.number_of_edges(), "avg degree %.5f"%(2*G.number_of_edges()/G.number_of_nodes()), "density %.9f"%nx.density(G))
print("avg clustering %.6f"%nx.average_clustering(G), "transitivity %.6f"%nx.transitivity(G))
comps = list(nx.connected_components(G)); lcc = max(comps, key=len)
print("components", len(comps), "isolates", nx.number_of_isolates(G), "LCC", len(lcc), "share %.4f"%(len(lcc)/G.number_of_nodes()))
print("avg shortest path LCC %.5f"%nx.average_shortest_path_length(G.subgraph(lcc)))
G2 = und([k for k in g.index if k[3]])
# keep all relation-network nodes to count isolates
G2.add_nodes_from(G.nodes())
print("excluding out-of-schema: edges", G2.number_of_edges(), "isolates", nx.number_of_isolates(G2))
cd = [k for k in g.index if k[2] in ("causal","description")]
print("causal/description typed groups:", len(cd))
D = nx.DiGraph()
for (s,t,rel,ok) in cd:
    D.add_node(s); D.add_node(t)
    if s!=t: D.add_edge(s,t)
print("directed subgraph: active nodes", D.number_of_nodes(), "unique directed connections", D.number_of_edges(), "self-loop groups", sum(1 for k in cd if k[0]==k[1]))
deg = sorted(G.degree, key=lambda x:-x[1])[:12]
print("top undirected degree:", deg)
