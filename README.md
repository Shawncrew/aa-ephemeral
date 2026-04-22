# aa-ephemeral

Alliance Auth Discord bot plugin that posts hidden fleet pings with a reveal button.
Only users who click the button see the secret message contents (ephemeral response).

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
