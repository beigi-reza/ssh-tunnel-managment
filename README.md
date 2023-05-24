# Manegment SSH tunnel and expose IT

![licence](https://img.shields.io/github/license/beigi-reza/ssh-tunnel)

This solution can be used for all methods for bypass limitations in highly restricted networks.

This program manage SSH tunnels between two Linux servers. The information of the tunnels read from a json file. This program can be run in UI and parameter mode (for scheduled execution).

for Use this program (solution), you need this:

- Upstream Server: A server that has access to the free Internet.
- Bridge Server: A server that is available to clients and has access to the upstream server (or upstream server access to Bridge Server)
 prerequisite
- The connection between the two servers must be through a key so that SSH connections can be managed without entering a password.

# Table of contents

- Definition
  - [Upstream Server](#upstream-server)
  - [bridge Server](#bridge-server)
- Config
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

## Upstream Server

A server that has access to the free Internet.

## Bridge Server

This server that is available to clients and has access to the upstream server

# Run on Bridge Server

In normal mode, SSH-Tunnel software runs on the bridge server.
On this mode, the SSH Tunnel Type must `locally` and the configuration of the ports is as follows

**Locally Mode**

```
User --> Bridge Server --> UpStream Server --> Free Internet
```

> Sample Config for `config.json`

```json
{
    "ssh_ip" : "192.168.1.1",
    "ssh_user" : "root",
    "ssh_port" : "22",
    "role_name": "Tunnle Name",
    "local_port": "8443",
    "destination_port": "3128",
    "type": "local"
}
```

`destination_port` of the upstream server is mounted on the `local_port` of the bridge server and the port is publicly available.

You can configure this configuration for each port

## Run on Upstream Server

If access to the **upstream server** is restricted or blocked `:(` but the **upstream server** can connect to the **bridge server**. You can change your connection mode and remove the created restriction

> Upstream Server Is Blocked

```
User --> Bridge Server --X UpStream Server --> Free Internet
```

> Use Remote SSH Tunnel

```
User --> Bridge Server <-- UpStream Server --> Free Internet
```

In this mode, the SSH-tunnle software must be run on both servers, on the upstream server in `remote` mode and on the bridge server in `local` mode.

### Step 1 (Run on Upstream Server)

The ports on the upstream server must be configured remotely.
In this mode, the `local_port` of the **upstream server** is mounted **locally** on the `destination_port` of the bridge server.

> Sample Config for `config.json`

```json
{
    "ssh_ip" : "192.168.1.1",
    "ssh_user" : "root",
    "ssh_port" : "22",
    "role_name": "Tunnle For Proxy",
    "local_port": "3158",
    "destination_port": "5128",
    "type": "remote"
}
```
### Step 2 (Run on Bridge Server)

The port opened in *Step 1* is opened locally on the **bridge server** and it is not possible to access it from Internet.
To resolve problem, this port should be bound on another port in **0.0.0.0** mode

There are two solutions to solve this problem The
- **first method:** SSH tunneling on this port on the **bridge server** 
- **second method:** Using the socat command and establish a relationship between two data sources

*In this document, we use the first method*

To open the port that was opened locally in **step 1**, create a tunnel on this port and IP **127.0.0.1** with the SSH tunnel program.
open port `local_port` on `0.0.0.0`

> Sample Config for `config.json`
```json
   {
  "ssh_ip" : "127.0.0.1",
  "ssh_user" : "root",
  "ssh_port" : "22",
  "role_name": "OutLine Expose",
  "local_port": "443",
  "destination_port": "5443",
  "type": "local"
 }
```

## Run SSH-tunnel

open `tu++.py` and  replace `<JSPATH>` with real path of `config.json`

```bash
vim tu++.py
```

find & Replace it 

```
JsFilePath = "<JSPATH>/config.json"
```
Save & Exit

run `tu++.py` on conole

```bash
cd ssh-tunnel
./tu++.py
```
- **u** : Status
- **s** : Start
- **d** : Drop/Kill

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
0 */4 * * *  /usr/bin/python3 /root/ssh-tunnel/tu++.py -r
```

