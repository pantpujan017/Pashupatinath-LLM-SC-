# Adapting LLM-SC to Living Sacred Heritage

Data, prompt and code for the paper *Adapting LLM-SC to Living Sacred Heritage: Domain-Specific Extraction, Semantic Networks and Human Evaluation on Pashupatinath Temple Reviews* by Pujan Pant, Sagar Newpane, Hari Sitaula and Manish Sakhakarmy.

GPT-4o was used to extract entities, aspect-level sentiments and relations from 2,500 English-language Tripadvisor reviews of Pashupatinath Temple, Kathmandu, Nepal. The extracted relations were then turned into semantic networks.

## Contents

| Path | Contents |
|---|---|
| `data/entity_mentions.csv` | 11,286 entity records (12 types) |
| `data/aspect_sentiments.csv` | 6,232 aspect-sentiment records (9 aspects) |
| `data/relations.csv` | 5,590 relation records |
| `data/README.md` | Column descriptions for the three files |
| `taxonomy/extraction_prompt.txt` | The prompt sent to GPT-4o (Appendix A of the paper) |
| `taxonomy/taxonomy_specification.md` | Entity types, relation types and aspect labels |
| `src/batch_extraction.py` | Extraction script (OpenAI Batch API) |
| `analysis/graph_counts.py` | Recomputes the network counts in Table 6 of the paper |
| `analysis/figure2.py` | Redraws Figure 2 of the paper |

## Quick start

You need Python 3 with pandas, NetworkX and matplotlib. The paper used Python 3.12, pandas 3.0.5 and NetworkX 3.6.1.

```bash
pip install pandas networkx matplotlib
python analysis/graph_counts.py data/
python analysis/figure2.py data/relations.csv figure2.png
```

`graph_counts.py` prints the node and edge counts reported in the paper. `figure2.py` draws every pair of concepts linked by at least seven relation records.

## Extraction script

`src/batch_extraction.py` shows how the model outputs were produced. It reads a CSV of reviews with `review_id` and `text_clean` columns, sends each review to GPT-4o with the prompt in `taxonomy/extraction_prompt.txt`, and saves each response, raw and parsed, to `llm_raw_outputs.jsonl`. To run it, install `openai`, `pandas` and `tqdm`, and replace `API_KEY` in the script with your own OpenAI key.

The review texts used in the study are not included, so the script cannot rebuild the released files on its own. Section 3.3.3 of the paper describes how the responses were parsed and exported.

## What is not included

The review texts are not redistributed, because reuse and redistribution rights for them have not been established. For the same reason, the supporting quotes, aspect evidence and relation descriptions produced during extraction are not released. Review IDs are pseudonymous keys (`R00001` to `R02491`).

## License

The code in `src/` and `analysis/` is released under the MIT License. The taxonomy and prompt in `taxonomy/` are released under CC BY 4.0. No licence is granted for the files in `data/`. See `LICENSE` for details.

## Citation

If you use these materials, please cite the paper above.
