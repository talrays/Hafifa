# Stock Price Mining Exercise - Multithreading

This exercise is based on a real case where the information was used for research on predicting stock prices using Twitter. For more details, feel free to reach out to Tomer.

## Part 1

The stock we want to track for hourly changes from the provided list of hours is Bitcoin. You are required to use multithreading to write a CSV file containing the following columns: hour, stock type, and the percentage change (increase/decrease) of the stock.

### Recommendations:
- Use `ThreadPoolExecutor` for multithreaded operations.
- Use the `yahooFinance` library to fetch stock price data.
- Use `pandas` to write the results to a CSV file.

The name of the CSV file should be retrieved from an environment variable called `DESTINATION_FILE`, and the path to the file containing the hours should be read from another environment variable.

## Part 2

In the first part, we focused only on Bitcoin. Now, adapt your existing code to handle multiple stock types. In addition to Bitcoin, include the stocks for Google and Amazon, and save all the data into the same CSV file created in Part 1.

### Environment Variables:
- **Amazon**: `AMAZON_DATES` (file: `amazon_dates.txt`)
- **Google**: `GOOGLE_DATES` (file: `google_dates.txt`)
- **Bitcoin**: `BITCOIN_DATES` (file: `bitcoin_dates.txt`)

## Good Luck! (:

---

# Implementation

Fetches minute OHLCV bars for BTC, GOOGL, and AMZN, keeps the minutes listed in each ticker’s timestamp file, and writes one CSV.

## Setup

Dependencies live in `pyproject.toml` (`yfinance`, `pandas`, `python-dotenv`). From this directory:

**Recommended ([uv](https://docs.astral.sh/uv/)):**

```bash
uv sync
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

`uv sync` creates `.venv` if needed and installs dependencies from `pyproject.toml`.

**Without uv:**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "yfinance>=0.2,<1" "pandas>=2.0,<3" "python-dotenv>=1.0,<2"
```

## Run

With the virtual environment active:

```bash
python main.py
```

`main.py` loads `.env`, builds a `Config`, and calls `run_pipeline`. Default logging is INFO with timestamps (`LOG_FORMAT` in `constants.py`). Set the root logger to DEBUG to see per-file timestamp parsing from `loader`.

## Configuration

`Config.from_env` reads:

| Variable | Default | Meaning |
| --- | --- | --- |
| `DESTINATION_FILE_PATH` | `output/output.csv` | CSV written by `write_report` (relative to the project directory) |
| `MAX_WORKERS` | `10` | Thread pool size for Yahoo downloads |

Tickers are defined in `models.StockTicker` (`BTC`, `GOOGL`, `AMZN`). Filename suffixes, the fetch window, and env defaults live in `constants.py`. Each ticker’s timestamps are read from `data/{TICKER}.txt` (`data/BTC.txt`, `data/GOOGL.txt`, `data/AMZN.txt`). Paths are resolved from the project directory (where `config.py` lives), not the shell’s current working directory.

## Data flow

```text
data/{TICKER}.txt
    -> loader.read_timestamps_from_txt   (parse, floor to the minute)
    -> Stock(required_timestamps)
    -> client.get_stock_data             (one thread-pool job per ticker)
    -> Stock.add_data
    -> Stock.get_required_data           (rows whose index is a required minute)
    -> report.build_report / write_report
```

`threads.run_in_parallel` submits every job to a `ThreadPoolExecutor` and returns futures in submission order. The pipeline reads each result after every job has finished, so one ticker's exception does not hide the others.

## Modules

| Module | Role |
| --- | --- |
| `main.py` | Process entry point. Logs a fatal error and exits 1 |
| `constants.py` | Env defaults, timestamp format, OHLCV columns, fetch window |
| `config.py` | `StockTicker` list, timestamp paths, output path, worker count |
| `loader.py` | Timestamp files into a `datetime` series |
| `models.py` | `StockTicker` enum (symbol list) and the `Stock` OHLCV frame |
| `client.py` | Yahoo Finance download, validation, and normalization |
| `errors.py` | `DownloadError` and `PipelineError` |
| `threads.py` | Thread pool runner. Returns futures; does not catch |
| `pipeline.py` | Wires load, fetch, filter, and write |
| `report.py` | Concatenates per-ticker frames and writes the CSV |

## Timestamp files

One timestamp per line:

```text
2026-06-15 13:15:59.919316
```

Parsed with `%Y-%m-%d %H:%M:%S.%f`, then floored to the minute. A missing file raises `FileNotFoundError`. A line that does not match, or a file with no lines, raises `ValueError`.

The latest timestamp in each file must fall within the last `MAX_FETCH_DAYS` (30), or Yahoo cannot serve that ticker. The pipeline checks every file before any download starts. If `data/BTC.txt` still lists dates from months ago while `data/GOOGL.txt` and `data/AMZN.txt` are recent, only BTC will fail with that rule.

## Runtime log trace (INFO)

A successful run roughly looks like:

```text
main          → Starting main
config        → Config loaded (tickers, destination, max_workers)
pipeline      → Starting pipeline
pipeline      → Loaded {TICKER} (minute count, file, fetch window)
threads       → Running N jobs in thread pool
client        → Downloading / Downloaded {TICKER} (bar counts)
pipeline      → Merged {TICKER} (downloaded vs required rows)
report        → Report slice per ticker, then file written with row count
pipeline      → Pipeline completed successfully
```

ERROR lines stay at `client` (chunk failures), `pipeline` (window/fetch abort), and `main` (fatal traceback).

## Errors

Leaves raise and do not log. The layer that decides to stop the run is the one that logs.

| Failure | Where it is raised | What happens |
| --- | --- | --- |
| Bad `MAX_WORKERS`, missing or unreadable timestamp file | `config`, `loader` | Propagates to `main` |
| End timestamp older than 30 days, or start after end | `validate_date_range` | Propagates out of that ticker's job |
| One 7-day chunk fails or is empty | `get_stock_data` | Logged and skipped |
| Chunk columns are not OHLCV | `get_stock_data` | `ValueError` for that ticker |
| Every chunk for a ticker was skipped | `DownloadError` | That ticker's job fails |
| Any ticker job failed | `pipeline` | Each ticker is logged, then `PipelineError`. The CSV is not written |
| Anything that escapes `run_pipeline` | `main` | `logger.exception`, exit status 1 |

## Yahoo Finance fetch

`get_stock_data` downloads `interval="1m"` bars from the earliest required timestamp through the latest.

- The end timestamp must fall within the last `MAX_FETCH_DAYS` (30).
- Longer ranges are clipped to that window. Minute history is requested in `CHUNK_DAYS` (7) chunks at `FETCH_INTERVAL` (`1m`).
- Indexes are converted to naive UTC and sorted. Rows must include `Open`, `High`, `Low`, `Close`, and `Volume`.
- A failed or empty chunk is logged and skipped. If every chunk is skipped, the ticker raises `DownloadError`.

Symbols sent to Yahoo are the enum values `BTC`, `GOOGL`, and `AMZN`.

## Output

`build_report` concatenates one row per required minute that has downloaded OHLCV, in ticker list order. Each row has `timestamp`, `stock_type` (enum value), and `price_change` (percent move from that minute's open to close). `write_report` writes those columns with `DataFrame.to_csv(..., index=False)` (`REPORT_COLUMNS`).
