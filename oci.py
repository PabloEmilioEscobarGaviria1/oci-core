#!/usr/bin/env python3
"""Local-first OCI knowledge and forecast registry; Python standard library only."""
import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("oci.db")
KINDS = ("fact", "hypothesis", "experiment", "observation", "source")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL, claim TEXT NOT NULL, source TEXT NOT NULL,
            confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            probability REAL NOT NULL CHECK(probability >= 0 AND probability <= 1),
            target_date TEXT NOT NULL, assumptions TEXT NOT NULL,
            outcome INTEGER CHECK(outcome IN (0, 1) OR outcome IS NULL),
            created_at TEXT NOT NULL
        );
        """)
    print(f"Initialized local database: {DB_PATH.resolve()}")


def add_knowledge(args):
    with connect() as db:
        cur = db.execute(
            "INSERT INTO knowledge(kind, claim, source, confidence, created_at) VALUES (?, ?, ?, ?, ?)",
            (args.kind, args.claim, args.source, args.confidence, now()))
        print(json.dumps({"id": cur.lastrowid, "status": "stored_locally"}))


def list_knowledge(_args):
    with connect() as db:
        rows = db.execute("SELECT * FROM knowledge ORDER BY id DESC").fetchall()
    for row in rows:
        print(json.dumps(dict(row), ensure_ascii=False))


def add_forecast(args):
    try:
        datetime.strptime(args.target_date, "%Y-%m-%d")
    except ValueError:
        raise SystemExit("target-date must use YYYY-MM-DD")
    with connect() as db:
        cur = db.execute(
            """INSERT INTO forecasts(question, probability, target_date, assumptions, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (args.question, args.probability, args.target_date, args.assumptions, now()))
        print(json.dumps({"id": cur.lastrowid, "status": "forecast_recorded"}))


def list_forecasts(_args):
    with connect() as db:
        rows = db.execute("SELECT * FROM forecasts ORDER BY id DESC").fetchall()
    for row in rows:
        print(json.dumps(dict(row), ensure_ascii=False))


def score_forecast(args):
    with connect() as db:
        row = db.execute("SELECT id FROM forecasts WHERE id = ?", (args.id,)).fetchone()
        if row is None:
            raise SystemExit(f"forecast id {args.id} not found")
        db.execute("UPDATE forecasts SET outcome = ? WHERE id = ?", (args.outcome, args.id))
        updated = db.execute("SELECT probability, outcome FROM forecasts WHERE id = ?", (args.id,)).fetchone()
    brier = (updated["probability"] - updated["outcome"]) ** 2
    print(json.dumps({"id": args.id, "outcome": updated["outcome"], "brier_score": round(brier, 6)}))


def build_parser():
    parser = argparse.ArgumentParser(description="OCI Core — local knowledge and forecast ledger")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init", help="create local database")
    p.set_defaults(func=lambda _a: init_db())
    p = sub.add_parser("add", help="add a knowledge item")
    p.add_argument("--claim", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--kind", choices=KINDS, default="hypothesis")
    p.add_argument("--confidence", type=float, default=0.5)
    p.set_defaults(func=add_knowledge)
    p = sub.add_parser("list", help="list knowledge items")
    p.set_defaults(func=list_knowledge)
    p = sub.add_parser("forecast", help="record a forecast")
    p.add_argument("--question", required=True)
    p.add_argument("--probability", type=float, required=True)
    p.add_argument("--target-date", required=True)
    p.add_argument("--assumptions", required=True)
    p.set_defaults(func=add_forecast)
    p = sub.add_parser("forecasts", help="list forecasts")
    p.set_defaults(func=list_forecasts)
    p = sub.add_parser("score", help="record binary outcome and calculate Brier score")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--outcome", type=int, choices=(0, 1), required=True)
    p.set_defaults(func=score_forecast)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "confidence") and not 0 <= args.confidence <= 1:
        parser.error("--confidence must be between 0 and 1")
    if hasattr(args, "probability") and not 0 <= args.probability <= 1:
        parser.error("--probability must be between 0 and 1")
    args.func(args)


if __name__ == "__main__":
    main()
