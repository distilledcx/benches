# Stealth Bench v2

[Browser Use's Stealth Bench v2](https://github.com/browser-use/benchmark/tree/74b427184d84b0df391a9c337def5aadf115a893/stealth_bench) has 100 sites behind bot protection. Each site gets two visits, and a judge model decides from screenshots whether the real site loaded within 60 seconds.

We ran the same frozen site list (dataset sha256 `6dee4f2e…3228`, upstream commit `74b4271`) from one Distilled cloud phone in Android Chrome.

## Results

| Run | Passed | Counted | Share | Share of all 200 |
| --- | --- | --- | --- | --- |
| Distilled with CAPTCHA solver | 197 | 197 | 100% | 98.5% |
| Distilled with no solver | 173 | 198 | 87.4% | 86.5% |

Other providers' numbers come from Browser Use's public `attempts.jsonl` at the same commit. We leave out site and network errors for every provider the same way.

## Exclusions

- `shs100-058`, both visits in both runs. The site returned a Cloudflare SSL 526 error.
- `shs100-075`, visit 2 in the solver run. The connection timed out.

See [results/distilled-solver/exclusions.json](results/distilled-solver/exclusions.json).

## Protocol

- **Visits.** 100 tasks × 2 repetitions, one at a time, each in a fresh incognito session.
- **Window.** Screenshots at 20 and 60 seconds after navigation starts.
- **No automation hooks.** No CDP attached, no proxy, no viewport or density override.
- **Judge, no solver.** Browser Use's judge, unchanged.
- **Judge, solver run.** `gpt-5.6-luna` at low effort. A visit passes when the site's content is on screen. A solved CAPTCHA with no page behind it doesn't pass.
- **Retries, solver run.** 15 visits were retried once after a failed or unclear first try. Every retry is marked with `retry_used`, and all 17 executed retry attempts are listed in `retries-all.jsonl`. Two retries turned a block into a pass. Under Browser Use's rule, which allows retries only for infrastructure failures, the solver score is 195 of 197.
- **Dates.** October 15 to 17, 2026. Browser Use's runs were on September 25, 2026.

## Files

| Path | Contents |
| --- | --- |
| `results/distilled-solver/attempts.jsonl` | One line per visit, 200 lines |
| `results/distilled-solver/retries-selected.jsonl` | The 15 retried visits as counted |
| `results/distilled-solver/retries-all.jsonl` | All 17 retry attempts with screenshot hashes |
| `results/distilled-solver/summary.json` | Totals by repetition |
| `results/distilled-solver/provenance.json` | Run settings and judge hashes |
| `results/distilled-no-solver/per-task.json` | Passed and counted visits per task |
| `data/vendors.json` | Our estimate of each task's bot protection |
| `data/site_order.json` | Browser Use's site-by-site column order, recovered from their chart |
| `data/final_data.json` | Everything the charts read |
| `charts/` | Rendered charts |
| `scripts/` | Scripts that build `data/` and `charts/` |

## Rebuilding

The scripts read Browser Use's public attempts file. Fetch it first.

```bash
curl -sLo data/attempts.jsonl https://raw.githubusercontent.com/browser-use/benchmark/74b427184d84b0df391a9c337def5aadf115a893/stealth_bench/official_results/attempts.jsonl
```

Then run `python3 scripts/order.py` and `python3 scripts/data.py` from this folder. `scripts/vendors.py` needs Browser Use's encrypted dataset in `private/` and sends one plain request to each site. The chart HTML needs the Distilled Sans font and vendor logos, which aren't included.
