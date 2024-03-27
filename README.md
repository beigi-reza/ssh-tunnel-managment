# Tunnels Manegment

![licence](https://img.shields.io/github/license/beigi-reza/ssh-tunnel)

This solution can be used for all methods for bypass limitations in highly restricted networks.

This program manage SSH tunnels between two Linux servers. Configuration of the tunnels read from a json file with the name `config.json`. This program can be run in Linux terminal and parameter mode (for scheduled execution).

for Use this program (solution), you need this:

- Upstream Server: A server that has access to the free Internet.
- Bridge Server: A server that is available to clients 
- One of Server access to another
- The connection between the two servers must be a key so that SSH connections.

# Table of contents

- Terminology
- Methods
  - [Run on Bridge Server](#run-on-bridge-server)
  - [Run on Upstream Server](#run-on-upstream-server)
    - [Step - 1 Run on Upstream Server](#step-1-run-on-upstream-server)
    - [Step - 2 Run on Bridge Server](#step-2-run-on-bridge-server)
- Prerequisite  
  - [setup ssh passwordless login](#setup-ssh-passwordless-login)
- Run
  - [Run SSH-tunnel](#run-ssh-tunnel)
  - [Run SSH-tunnel with parameter](#run-ssh-tunnel-with-parameter)
- [Scheduled SSH-Tunnel](#scheduled-ssh-tunnel)


## Terminology

- **Upstream Server** : A server that has access to the free Internet.

- **Bridge Server** : This server that is available to Clients
- **Client** : A user-side application with access to the bridge server.

## Methods

### Bridge server access to the upstream server

```
(Client) <-> [ Bridge Server ] <-> [ Upstream Server ] <-> (Internet)
```

in This method, the Tunnel-Managment software runs on the **bridge server** and the bridge server must be able to ssh access to the upstream server

in `config.json` parameter `upstream_is_Block` set **`false`**

```json
"upstream_is_Block": false,    
```

### upstream server is Blocked but but it can Connect to Bridge server 

- If upstream server is blocked 
- If connect to upstream, it will be blocked

```
(Client) <-> [ Bridge Server ] <-X [ Upstream Server ] <-> (Internet)
```
in This method, the Tunnel-Managment software runs on the **Upstream server** and must be able to ssh access to the bridge server 

in `config.json` parameter `upstream_is_Block` set **`true`**

```json
"upstream_is_Block": true,
```


## Run & Config


### Destination Server
Update Detination Server ssh config in File `config.json` section `Dest_Server`

```json
{
    "Dest_Server":{
        "ip" : "10.1.8.180",
        "user" : "root",
        "port" : "22"
    },
}
```

- If you run the software on the bridge server and `upstream_is_Block` set to `false`, your destination server will be Upstream server

- If you run the software on the upstream server and `upstream_is_Block` set to `true`, your destination server will be bridge server


### Tunnel Data

Add this section once for each (tunnel) port
```json
        {
            "role_name": "Mongo EXpress",
            "local_port": "9091",
            "destination_port": "8081"
        }
```

- if parameter `upstream_is_Block` set `false`

```
[ Bridge Server:Local_port ] --> [ Upstream Server:destination_port ]
```

if parameter `upstream_is_Block` set `true`

```
[ Bridge Server:Local_port ] <-- [ Upstream Server:destination_port ]
```

### Update Config Path

open `sshTunnel.py` and  replace `<JSPATH>` with real path of `config.json`


## Run 
run `sshTunnel.py` on conole

```bash
cd ssh-tunnel-managment
./sshTunnel.py
```
- **u** : Status
- **s** : Start
- **d** : Drop/Kill
- **h** : help

## Run SSH-tunnel with parameter

- `tu++.py` for run in UI Mode
- `tu++.py` `-s` for start All tunnel/s
- `tu++.py` `-u` for Chek Status of tunnel/s
- `tu++.py` `-d` for Drop/kill all tunnel/s
- `tu++.py` `-r` for Restart ( Drop & Start) all tunnel/s


# Scheduled SSH-Tunnel

It is possible that the SSH tunnels will be closed after some time and the servers will be disconnected, or the servers will be detected due to the long duration of a tunnel.
To solve this issue, kill & Run the SSH-Tunnel with cron service.

```bash
crontab -e
```

add this line for restart(Kill & Start) tunnel every 4 hours

```
0 */4 * * *  /usr/bin/python3 /root/ssh-tunnel-managment/sshTunnel.py -r
```

