#!/usr/bin/env python3
"""Luma → Telegram: постит AI-события Лондона в канал «luma london».

Источник: публичный discover-API Luma (api.luma.com, без ключей),
категория cat-ai + координаты Лондона. Дважды в сутки и чаще (POLL_HOURS)
постит новые события; по понедельникам — дайджест недели.

Usage:
  TG_BOT_TOKEN=... TG_CHAT_ID=-100... python3 luma_london_ai_bot.py --once
  ... --digest   # форс-дайджест недели
  ... --loop     # вечный цикл (режим для docker)

Env:
  TG_BOT_TOKEN  токен бота (обязателен)
  TG_CHAT_ID    chat_id канала (обязателен)
  STATE_FILE    путь к state-файлу (default /data/state.json)
  POLL_HOURS    период проверки в --loop (default 6)

Секреты читаются только из окружения — не хардкодить и не коммитить.
Деплой: см. scripts/luma_bot.Dockerfile (eva02, docker --restart unless-stopped).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

LUMA_API = "https://api.luma.com/discover/get-paginated-events"
CATEGORY = "cat-ai"
LONDON_LAT, LONDON_LON = 51.5074, -0.1278
HORIZON_DAYS = 60
PAGE_LIMIT = 25
MAX_PAGES = 20
TG_MSG_LIMIT = 4096
LONDON_TZ = ZoneInfo("Europe/London")

STATE_FILE = os.environ.get("STATE_FILE", "/data/state.json")
POLL_HOURS = float(os.environ.get("POLL_HOURS", "6"))

WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
MONTHS_RU = ["янв", "фев", "мар", "апр", "мая", "июн",
             "июл", "авг", "сен", "окт", "ноя", "дек"]


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] {msg}", flush=True)


def http_json(url: str, data: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "luma-london-bot/1.0"})
    if data is not None:
        req.data = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_events() -> list[dict]:
    """Все офлайн AI-события Лондона на ближайшие HORIZON_DAYS дней."""
    now = datetime.now(timezone.utc)
    horizon = now + timedelta(days=HORIZON_DAYS)
    events: dict[str, dict] = {}
    cursor = None
    for _ in range(MAX_PAGES):
        params = {
            "discover_category_api_id": CATEGORY,
            "latitude": LONDON_LAT,
            "longitude": LONDON_LON,
            "pagination_limit": PAGE_LIMIT,
        }
        if cursor:
            params["pagination_cursor"] = cursor
        page = http_json(f"{LUMA_API}?{urllib.parse.urlencode(params)}")
        for entry in page.get("entries", []):
            ev = entry.get("event") or {}
            start = ev.get("start_at")
            geo = ev.get("geo_address_info") or {}
            if not start or not ev.get("api_id"):
                continue
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            if start_dt < now or start_dt > horizon:
                continue
            if ev.get("location_type") != "offline" or geo.get("city") != "London":
                continue
            events[ev["api_id"]] = {
                "api_id": ev["api_id"],
                "name": ev.get("name", "(без названия)"),
                "start_at": start,
                "address": geo.get("short_address") or geo.get("address") or "",
                "url": f"https://luma.com/{ev.get('url', '')}",
            }
        cursor = page.get("next_cursor")
        if not page.get("has_more") or not cursor:
            break
        # события идут по возрастанию даты — за горизонтом можно остановиться
        entries = page.get("entries", [])
        if entries:
            last = (entries[-1].get("event") or {}).get("start_at")
            if last and datetime.fromisoformat(last.replace("Z", "+00:00")) > horizon:
                break
    return sorted(events.values(), key=lambda e: e["start_at"])


def load_state() -> dict:
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"seen": {}, "last_digest": None}


def save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_FILE)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_event(ev: dict) -> str:
    dt = datetime.fromisoformat(ev["start_at"].replace("Z", "+00:00")).astimezone(LONDON_TZ)
    when = f"{WEEKDAYS_RU[dt.weekday()]} {dt.day} {MONTHS_RU[dt.month - 1]}, {dt:%H:%M}"
    line = f"• <b>{when}</b> — <a href=\"{esc(ev['url'])}\">{esc(ev['name'])}</a>"
    if ev["address"]:
        line += f"\n  📍 {esc(ev['address'])}"
    return line


def send_message(text: str) -> None:
    token = os.environ["TG_BOT_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    resp = http_json(
        f"https://api.telegram.org/bot{token}/sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        },
    )
    if not resp.get("ok"):
        raise RuntimeError(f"telegram error: {resp}")


def send_chunked(header: str, lines: list[str]) -> None:
    chunk = header
    for line in lines:
        piece = "\n\n" + line
        if len(chunk) + len(piece) > TG_MSG_LIMIT:
            send_message(chunk)
            chunk = header + " (продолжение)" + piece
        else:
            chunk += piece
    send_message(chunk)


def post_new_events(events: list[dict], state: dict) -> int:
    new = [ev for ev in events if ev["api_id"] not in state["seen"]]
    if new:
        send_chunked("🆕 <b>Новые AI-события в Лондоне</b>", [fmt_event(e) for e in new])
    for ev in new:
        state["seen"][ev["api_id"]] = ev["start_at"]
    return len(new)


def post_digest(events: list[dict], state: dict) -> int:
    week_end = datetime.now(timezone.utc) + timedelta(days=7)
    week = [
        ev for ev in events
        if datetime.fromisoformat(ev["start_at"].replace("Z", "+00:00")) <= week_end
    ]
    if week:
        send_chunked("📅 <b>AI-события Лондона на неделю</b>", [fmt_event(e) for e in week])
    state["last_digest"] = datetime.now(LONDON_TZ).strftime("%G-W%V")
    return len(week)


def prune_state(state: dict) -> None:
    now = datetime.now(timezone.utc)
    state["seen"] = {
        k: v for k, v in state["seen"].items()
        if datetime.fromisoformat(v.replace("Z", "+00:00")) > now - timedelta(days=7)
    }


def run_cycle(force_digest: bool = False) -> None:
    state = load_state()
    events = fetch_events()
    log(f"fetched {len(events)} upcoming London AI events")

    n_new = post_new_events(events, state)
    log(f"posted {n_new} new events")

    now_london = datetime.now(LONDON_TZ)
    this_week = now_london.strftime("%G-W%V")
    if force_digest or (now_london.weekday() == 0 and state.get("last_digest") != this_week):
        n_week = post_digest(events, state)
        log(f"posted weekly digest with {n_week} events")

    prune_state(state)
    save_state(state)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--once"
    if mode == "--loop":
        log(f"loop mode: polling every {POLL_HOURS}h, state={STATE_FILE}")
        while True:
            try:
                run_cycle()
            except Exception as e:  # переживаем сетевые сбои, docker нас не перезапускает зря
                log(f"cycle failed: {e!r}")
            time.sleep(POLL_HOURS * 3600)
    elif mode == "--digest":
        run_cycle(force_digest=True)
    elif mode == "--once":
        run_cycle()
    else:
        sys.exit(f"unknown mode {mode}; use --once | --digest | --loop")


if __name__ == "__main__":
    main()
