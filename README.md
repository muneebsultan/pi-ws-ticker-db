# pi-ws-ticker-db

Small **Raspberry Pi**–oriented project for **ticker** data: ingest from exchange APIs, optionally over **WebSockets**, and **persist** to storage (file or database).

## What this repo is for

- Run lightweight collectors on a Pi (low idle cost, always-on).
- Prefer streaming (**WebSockets**) for frequent updates; use a **database** when you outgrow append-only JSON.
- Keep dependencies minimal so builds work on ARM (`aarch64` / `armv7`).

## Current implementation

The included script `database_writing.py` is a **starting point**: it polls Binance **REST** (`/api/v3/ticker/price`) for a fixed list of symbols, adds a Unix timestamp, and **appends JSON lines** to `data.json`.

Planned direction (aligned with the name **pi-ws-ticker-db**):

1. Switch price updates to Binance **WebSocket** streams (lower overhead than polling).
2. Replace or complement the JSON file with a real **DB** (e.g. SQLite or Postgres) via SQLAlchemy.

## Requirements

- Python 3.7+ (matches `dockerfile`)
- Network access to `https://api.binance.com` (public endpoints; no API key for this sample)

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python database_writing.py
```

Edit symbols in `database_writing.py`:

```python
pairs = ["XLMUSDT", "LINKUSDT", "LTCUSDT"]
file_name = "./data.json"
```

Stop with `Ctrl+C`.

## Run with Docker

Ensure `data.json` exists in the project root (can be an empty file) so the image build can `COPY` it.

```bash
docker compose up --build
```

Compose runs `python ./database_writing.py` and mounts `data.json` so data survives container restarts. Adjust the volume target in `docker-compose.yml` if your mount path differs from `/app/data.json`.

## Project layout

| Path | Role |
|------|------|
| `database_writing.py` | Ticker fetch loop (REST → JSON today) |
| `requirements.txt` | Python dependencies |
| `dockerfile` / `docker-compose.yml` | Container run |
| `data.json` | Append-only output (created/grown at runtime) |

## Notes

- **Rate limits:** REST polling in a tight loop can hit exchange limits if you add many pairs or shorten sleeps; WebSockets are the intended fix.
- **JSON validity:** Appending `json.dump` per line with trailing commas produces JSONL-like lines; if you need strict JSON arrays, normalize with a separate export step or move to a database.

## License

Add a license file if you publish this repository (e.g. MIT).
