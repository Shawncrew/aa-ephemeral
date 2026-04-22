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
