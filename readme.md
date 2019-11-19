# Raspberry Pi JSON API

## Requirements

- `members`: `sudo apt-get install members`

## Running

```sh
python app.py
```

## Routes

- `/`: API Version
- `/disk`: List disk partitions with details
- `/group/<gid|name>`: Show group info
- `/groups`: List all groups
- `/interfaces`: List network interfaces
- `/user/<uid|name>`: Show user info
- `/users`: List all users
