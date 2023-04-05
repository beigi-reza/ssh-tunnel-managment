# Tunnel port & Expose

![licence](https://img.shields.io/github/license/beigi-reza/ssh-tunnel)

This solution can be used for all methods for bypass limitations in highly restricted networks.

This program manage SSH tunnels between two Linux servers. The information of the tunnels read from a json file. This program can be run in UI and parameter mode (for scheduled execution).

for Use this program (solution), you need this:
 - Upstream Server: A server that has access to the free Internet.
 - Bridge Server: A server that is available to clients and has access to the upstream server (or upstream server access to Bridge Server)
 prerequisite
- The connection between the two servers must be through a key so that SSH connections can be managed without entering a password.

# Table of contents

- [Upstream Servrt](#upstream-server)
  - [install bypass limitations Application ]()



## Upstream Server
A server that has access to the free Internet.

### install bypass limitations Application
Install your favorite software to bypass internet restrictions on the server, this program has been tested with the following software.
 - [Outline](https://getoutline.org/)
 - [shadowsocks](https://shadowsocks.org/)
 - [v2ray(VMESS)](https://github.com/beigi-reza/v2ray-docker-compose)
 - [Squid proxy](https://github.com/beigi-reza/docker-compose-squid)
 - [OpenConnect(ocserv)](https://github.com/beigi-reza/docker-compose-ocserv)


## Bridge Server
This server that is available to clients and has access to the upstream server


## Setup SSH Passwordless Login
to run this script without any problems, it is better for connect servers use SSH KEY so that you are not asked for a password for each connection.

### Create Authentication SSH-Keygen Keys

```cmd
ssh-keygen -t rsa
```
![ssh-keygen](https://www.tecmint.com/wp-content/uploads/2012/10/Create-SSH-RSA-Key.gif)

### Upload SSH Key to `Destination Server`

```cmd
ssh-copy-id root@192.168.0.11
```
### Test SSH Passwordless Login

```cmd
ssh sheena@192.168.0.11
```
![ssh](https://www.tecmint.com/wp-content/uploads/2012/10/SSH-Remote-Passwordless-Login.gif)


### FnSshPortForwardind
This function creates a tunnel between the destination server and this server and mounts port `<destination-port>` from the destination server on port `<local-port>` from the source server.

## PreRun

Replace the following variables in the script file  with appropriate values

- ‍‍`DestinationIP=<IP>`  The destination server we want to connect to
- `DestinationPort=<PORT>` SSH port of destination server

in function **`fnStart`** 


For each port you want to open, repeat this line and set the value

- `FnSshPortForwardind <local-port> <destination-port>`

`<destination-port>` : The destination port on the destination server
`<local-port>‍ ` : The port that is opened locally on this server for ssh tunnel

## Run 

```cmd
./tunnel++.sh 
```

- **`c`** for check active **ssh tunnel** and **bidirectional data transfers** to Destination Server
- **`s`** Start Tunnel and Bind Port/s to `0.0.0.0` as backgrund Process
- **`k`** kill all **ssh tunnel** and **bidirectional data transfers** 

