# Raspberry Pi JSON API

## Requirements

- `members`: `sudo apt-get install members`

## Running

```sh
python app.py
```

## Routes

| Path           | Method  | Arguments                                                                                                                                                                       | Description                               |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| `/`            | GET     |                                                                                                                                                                                 | API stattus and version                   |
| `/groups/:gid` | GET     | `gid` or `groupname`                                                                                                                                                            | Show info of `groupname` or `gid`         |
| `/groups`      | GET     |                                                                                                                                                                                 | List all groups                           |
| `/user/:uid`   | GET     | `uid` or `username`                                                                                                                                                             | Show info of `uid` or `username`          |
| `/users`       | GET     |                                                                                                                                                                                 | List all users                            |
| `/cpu`         | GET     |                                                                                                                                                                                 | CPU information                           |
| `/uptime`      | GET     |                                                                                                                                                                                 | Uptime in seconds (`idletime` + `uptime`) |
| `/hostname`    | GET     |                                                                                                                                                                                 | Hostname `fqdn` and local `ip` address    |
| `/kernel`      | GET     |                                                                                                                                                                                 | Kernel and kernel modules info + version  |
| `/shells`      | GET     |                                                                                                                                                                                 | Available/installed shells                |
| `/ssh`         | GET     |                                                                                                                                                                                 | Host's public ssh keys                    |
| `/block`       | GET     |                                                                                                                                                                                 | Block device list + information           |
| `/useradd`     | POST    | `name` - `string` - username of the new user<br/>`groups` - `array<string>` - list of groups the new user will be member of<br/>`password` - `string` - the new user's password | Create new user                           |
| `/deluser`     | DELETE  | `name` - `string` - username to delete                                                                                                                                          | Delete user                               |
| `/groupadd`    | POST    | `name` - `string` - the group name                                                                                                                                              | Create a new `name` group                 |
| `/delgroup`    | POST    | `name` - `string` - the group to be deleted                                                                                                                                     | Delete the group `name`                   |
| `/userlock`    | POST    | `name` - `string` - the user to lock                                                                                                                                            | Lock a user                               |
| `/userunlock`  | POST    | `name` - `string` - the user to unlock                                                                                                                                          | Unlock a user                             |
| <!--           | `/net`  | GET                                                                                                                                                                             |                                           | List network interfaces | --> |
| <!--           | `/disk` | GET                                                                                                                                                                             |                                           | List disk partitions with details | --> |
