import paramiko
from sshtunnel import SSHTunnelForwarder

def establish_tunnel(ssh_host, ssh_port, ssh_username, ssh_password, remote_host, remote_port):
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=(remote_host, remote_port)
    ) as tunnel:
        print(f"Tunnel established to {ssh_host}:{ssh_port} -> {remote_host}:{remote_port}")

        # You can perform operations through the tunnel here
        # For example, you can establish an SSH connection over the tunnel
        
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the tunnel
            ssh_client.connect(hostname='localhost', port=tunnel.local_bind_port, username=ssh_username, password=ssh_password)

            # Perform operations on the server via the tunnel
            # For example, execute a command:
            stdin, stdout, stderr = ssh_client.exec_command("ls -l")

            # Print the output
            for line in stdout:
                print(line.strip())

        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as e:
            print(f"Unable to establish SSH connection: {e}")
        finally:
            # Close the SSH connection
            ssh_client.close()

# Define SSH tunnel and remote server details
ssh_host = '10.1.8.180'
ssh_port = 22  # default SSH port
ssh_username = 'root'
ssh_password = '&JJP6JCP3DRs&i6STyq'
remote_host = '127.0.0.1'
remote_port = 22  # SSH port on the remote server

# Establish tunnel and perform operations
establish_tunnel(ssh_host, ssh_port, ssh_username, ssh_password, remote_host, remote_port)
