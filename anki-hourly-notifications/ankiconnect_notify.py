"""
Optionales Bonus-Script: fragt über AnkiConnect (Anki Desktop) die Anzahl
faelliger Karten ab und schickt bei Bedarf eine Push-Benachrichtigung ans
iPhone ueber ntfy.sh.

Voraussetzungen:
- Anki Desktop laeuft, AnkiConnect-Addon (Code 2055492159) installiert
- ntfy App auf dem iPhone, ein (moeglichst einzigartiges) Topic abonniert
- pip install -r requirements.txt

Aufruf:
    python ankiconnect_notify.py --topic dein-eindeutiges-topic

Fuer die stuendliche Ausfuehrung per Windows-Aufgabenplanung einplanen.
"""

import argparse
import sys

import requests

ANKICONNECT_URL = "http://127.0.0.1:8765"


def get_due_card_count(deck_query: str = "is:due -is:suspended") -> int:
    response = requests.post(
        ANKICONNECT_URL,
        json={
            "action": "findCards",
            "version": 6,
            "params": {"query": deck_query},
        },
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("error"):
        raise RuntimeError(f"AnkiConnect-Fehler: {payload['error']}")
    return len(payload["result"])


def send_ntfy_notification(topic: str, due_count: int) -> None:
    requests.post(
        f"https://ntfy.sh/{topic}",
        data=f"Du hast noch {due_count} faellige Anki-Karte(n) offen.".encode("utf-8"),
        headers={
            "Title": "Anki Karten faellig",
            "Priority": "default",
            "Tags": "books",
        },
        timeout=10,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--topic", required=True, help="ntfy.sh Topic-Name (frei waehlbar, eindeutig)"
    )
    parser.add_argument(
        "--query",
        default="is:due -is:suspended",
        help="Anki-Suchfilter fuer faellige Karten (Standard: is:due -is:suspended)",
    )
    args = parser.parse_args()

    try:
        due_count = get_due_card_count(args.query)
    except requests.exceptions.ConnectionError:
        print(
            "Konnte AnkiConnect nicht erreichen. Laeuft Anki Desktop mit "
            "installiertem AnkiConnect-Addon?",
            file=sys.stderr,
        )
        return 1

    print(f"Faellige Karten: {due_count}")

    if due_count > 0:
        send_ntfy_notification(args.topic, due_count)
        print("Benachrichtigung gesendet.")
    else:
        print("Keine faelligen Karten, keine Benachrichtigung noetig.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
