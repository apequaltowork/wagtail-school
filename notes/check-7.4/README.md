# 7.4 check against the 2.7 baseline

Produced by `tools/baseline.py --base http://127.0.0.1:8074 --out notes/check-7.4 --compare baseline`.

| File | Result |
|---|---|
| urls.txt | identical (55 URLs, same statuses) |
| counts.json | identical |
| form_field_keys.json | identical (2.7 hyphenated keys still stored and used) |
| form_submissions_*.csv | identical, byte for byte (admin export via `?export=csv`) |
| page_text.json | 49 of 51 pages identical. **Expected differences:** `/search/?query=music` and `/search/?query=scholarship` return more results with the `database` search backend (UPGRADE_LOG B18). |

Every StreamField page's visible text matches 2.7, so the content survived text → jsonb (B15).
