# aa-ephemeral

Alliance Auth Discord bot plugin that posts hidden fleet pings with a reveal button.
Only users who click the button see the secret message contents (ephemeral response).

## Dependencies

- [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) >= 3
- [allianceauth-discordbot](https://github.com/Solar-Helix-Independent-Transport/allianceauth-discordbot) >= 5
- [py-cord](https://github.com/Pycord-Development/pycord) >= 2

## Installation

Add to your `requirements.txt`:

```
git+https://github.com/Shawncrew/aa-ephemeral.git
```

Add to `INSTALLED_APPS` in `local.py`:

```python
"aa_ephemeral",
```

Run migrations:

```bash
python manage.py migrate aa_ephemeral
```

Assign the `aa_ephemeral | Fleet Ping | Can send hidden fleet pings` permission to the Auth group whose members should be able to use `/fleetping`.

## Usage

```
/fleetping #channel <secret message>
```

Posts a public `@everyone` embed in `#channel` with an **Open** button. Only users who click the button receive the secret message — ephemerally, visible to them alone.

Each ephemeral reveal contains:
- The secret message text (with an invisible watermark unique to the recipient)
- `Sent by: <FC name> at 2026-04-22 04:10:00125208` — the trailing 6 digits are a unique identifier for the recipient, disguised as a sub-second timestamp component

## Leak Identification

Every ephemeral reveal is watermarked with two layers tied to the recipient's Discord account:

**Invisible watermark** — zero-width Unicode characters embedded silently inside the message text. Survives copy-paste to any platform.

**Visible msgid** — a short code shown at the bottom of the reveal (e.g. `A3F2B1C4`).

### Identifying a leak from copy-pasted text

If a user forwards the message text to another channel, paste it into the management command:

```bash
docker compose exec allianceauth_gunicorn python manage.py identify_leak <message_id> "pasted message text here"
```

### Identifying a leak from a screenshot

If only a screenshot is available, use the 6-digit code at the end of the timestamp:

```bash
docker compose exec allianceauth_gunicorn python manage.py identify_leak <message_id> --code 125208
```

Both commands output the matching Auth username and email address.
