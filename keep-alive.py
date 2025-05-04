#! /usr/bin/python3

import lib.BaseFunction
import tunnel as tu
import concurrent.futures
from datetime import datetime, timedelta
import os
from tunnel import ( 
    TUNNEL_LIST,current_directory
)


#def autostart(TUNNEL_LIST):
#    with concurrent.futures.ProcessPoolExecutor() as executor:    
##        for tunnel in TUNNEL_LIST:
##            future_to_id = executor.submit(tu.FnAutorestartTunnel(tunnel))    
##            tu.FnStartTunnel(tunnel)
#        
#        future_to_id = {executor.submit(tu.FnAutoRestartTunnel, tunnel): tunnel for tunnel in TUNNEL_LIST}
#        #future_to_id = {executor.submit(worker_process, i): i for i in range(num_processes)}
#
#        for future in concurrent.futures.as_completed(future_to_id):
#            process_id = future_to_id[future]
#            try:
#                result = future.result()
#                print(f"Received: {result}")
#            except Exception as e:
#                print(f"Process {process_id} generated an exception: {e}")


def KeepAliveList():
    _tunnel = []
    for tunnel in TUNNEL_LIST:
        if tunnel.get('Keep_Alive',False):
            _tunnel.append(tunnel)
    return _tunnel
def FnStartTthread(KeepAliveTunnelList):
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(KeepAliveTunnelList)) as executor:    
        future_to_tunnel = {executor.submit(tu.FnAutoRestartTunnel, tunnel): tunnel for tunnel in KeepAliveTunnelList}
        try:
            for future in concurrent.futures.as_completed(future_to_tunnel):
                tunnel = future_to_tunnel[future]
                try:
                    result = future.result()
                    print(f"Tunnel thread for {tunnel.name} completed with: {result}")
                except Exception as e:
                    print(f"Tunnel {tunnel.name} generated an exception: {str(e)}")
        except KeyboardInterrupt:
            print("Shutting down all tunnels...")


if __name__ == "__main__":    
    logpath  = os.path.join(current_directory,'logs')
    if os.path.exists(logpath) == False:
        _log = f'Logs Folder not found [ {logpath} ]'
        print (f"{_log}")        
        lib.BaseFunction.FnExit()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _LineLog = f"### {timestamp},Trying Started Tunnel as Keep Alive Mode ..."
    print (f"{_LineLog}")
    tu.SaveLogWebsite(_LineLog)
    #autostart(TUNNEL_LIST)
    KeepAliveTunnelList = KeepAliveList()
    if len(KeepAliveTunnelList) == 0:
        _LineLog = f"### {timestamp},The keep-alive option is not enabled for any tunnel."
        print (f"{_LineLog}")
        tu.SaveLogWebsite(_LineLog)
    else:
        FnStartTthread(KeepAliveTunnelList)