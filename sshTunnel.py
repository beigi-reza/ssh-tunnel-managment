#! /usr/bin/python3
from colorama import Fore, Back, Style
from datetime import datetime
import sys
import os
import json
import signal
import socket

_B = Style.BRIGHT
_N = Style.NORMAL
_D = Style.DIM
_w = Fore.WHITE
_y = Fore.YELLOW
_b = Fore.BLUE
_r = Fore.RED
_c = Fore.CYAN
_g = Fore.GREEN
_reset = Style.RESET_ALL


## ONLY IN Run Stand Alone
JsFilePath = "/home/beigi/Github/ssh-tunnel-managment/config.json"

##################################################
##################################################

def handler(signum, frame):
   print("")
   print(Style.NORMAL + Fore.RED + " Force Exit By press [ " + Fore.WHITE + "CTRL + C" + Fore.RED + " ]")
   print("")
   FnExit()

def FnExit():          
   print (Style.NORMAL + Fore.WHITE + "Bye :)")        
   sys.exit()



#def FnBanner():
#   print (Fore.BLUE + "    ______  ______                       __        ______   " + Fore.RESET)
#   print (Fore.CYAN + "   / / / / /_  __/_  ______  ____  ___  / / __    _\ \ \ \  " + Fore.RESET)
#   print (Fore.GREEN + "  / / / /   / / / / / / __ \/ __ \/ _ \/ /_/ /___/ /\ \ \ \ " + Fore.RESET)
#   print (Fore.RED + "  \ \ \ \  / / / /_/ / / / / / / /  __/ /_  __/_  __/ / / / " + Fore.RESET)
#   print (Fore.YELLOW + "   \_\_\_\/_/  \__,_/_/ /_/_/ /_/\___/_/ /_/   /_/ /_/_/_/  " + Fore.RESET)
#   print (Fore.MAGENTA + "                                                            " + Fore.RESET)

def FnPrintMenu():
   print("")
   print (Style.DIM + "press 'q' for quit" + Style.RESET_ALL)        
   print (Style.DIM + "press 'h' for help" + Style.RESET_ALL)        
   usrInput = input(Style.BRIGHT + "Command Mode ( " + Fore.BLUE + "Status [ " + Fore.YELLOW + "*U*" + Fore.BLUE + " ] Sart [ " + Fore.YELLOW + "S" + Fore.BLUE + " ] / Drop/Kill  [ " + Fore.YELLOW + "D" + Fore.BLUE + " ]"+ Fore.RESET + " ) : " + Style.RESET_ALL)
   try:  
      usrInput = usrInput[0] 
   except:
      usrInput = "u"  

   if usrInput.lower() == "u":     
      PrintServerDetail()
      FnCheckStatus()
   elif usrInput.lower() == "s":   
      FnStartTunnle()
   elif usrInput.lower() == "d":      
      FnKillAllProcess()
   elif usrInput.lower() == "q":      
      sys.exit()
   elif usrInput.lower() == "h":
      lib.clearScreen()
      bannerlib.GetBanner()
      Fnhelp()       
      FnPrintMenu()
   else: 
      os.system('clear')
      print ("-----------------------")
      print (Style.BRIGHT + Fore.BLACK + Back.WHITE + "(" + usrInput + ") is Not Valid Code ")  
      print (Style.RESET_ALL + "-----------------------")
      FnPrintMenu()

def FnLoadJsonFile():
   try:
      JsFile = open(JsFilePath, "r")
   except:
      print(Fore.RED + "Json File Not Found " + Fore.RESET)  
      sys.exit()
   
   js = JsFile.read()
   js  = js.replace('\n', '') 
   global JsonConfig
   JsonConfig = json.loads(js)    


def GetSignalTunnle(UserInput):
   try:
      _userget = int(UserInput)
   except:
      _userget = UserInput
   ListOfTunnel = JsonConfig["tunnel"]   
   if type(_userget) is int :
      if _userget == 0:
         return False
      if _userget <= len(ListOfTunnel):
         return ListOfTunnel[_userget-1]
      else:
         return False
   if type(_userget) is str:
      for _ in ListOfTunnel:
         if _["role_name"].strip().lower() == _userget.lower().strip():
            return _
      return False   
         
   
#def FnStartSingleTunnle(TunnleDict:dict):
#   # این فانکشن برای سازگاری با نگارش قدیم و نرم افزار SSH Managment باقی مانده است
#   TName = TunnleDict["role_name"]
#   Tlocal_port = TunnleDict["local_port"]
#   TDestinationPort = TunnleDict["destination_port"]   
#   # Ttype = TunnleDict["type"]
#   Ttype = RunInUpStream
#   TSSHIp = TunnleDict["ssh_ip"]
#   TSSHPort = TunnleDict["ssh_port"]
#   TSSHUser = TunnleDict["ssh_user"]
#   if Ttype == "local":
#      print (Style.BRIGHT + Fore.WHITE + "Tunneling Port [ " + Fore.RED + TDestinationPort + Fore.WHITE + " ] Server [ " + Fore.RED + TSSHIp + Fore.WHITE + " ] to [ " + Fore.RED + Tlocal_port + Fore.WHITE + " ] server Local for [ " + Fore.BLUE + TName + Fore.WHITE + " ]" + Style.RESET_ALL )               
#      Command = "sudo ssh -NTC -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -f -N -p {SSHPort} {SSHUser}@{SSHIp} -L 0.0.0.0:{local_port}:0.0.0.0:{DestinationPort}"
#      Command = Command.format(SSHPort = TSSHPort, SSHUser = TSSHUser, SSHIp = TSSHIp, local_port = Tlocal_port, DestinationPort = TDestinationPort )
#      os.system(Command)                                        
#      Logit("start-local")
#   elif Ttype == "remote":               
#      print (Style.BRIGHT + Fore.WHITE + "Remote Tunneling port [ " + Fore.RED + Tlocal_port + Fore.WHITE + " ] local server to server [ " + Fore.RED + TSSHIp + Fore.WHITE + " ] port [ " + Fore.RED + TDestinationPort + Fore.WHITE + " ] for [ " + Fore.BLUE + TName + " ] " + Style.RESET_ALL)
#      Command = "ssh -R 0.0.0.0:{DestinationPort}:127.0.0.1:{local_port} -N -f -p {SSHPort} {SSHUser}@{SSHIp}"
#      Command = Command.format(DestinationPort = TDestinationPort, local_port = Tlocal_port, SSHPort = TSSHPort, SSHUser = TSSHUser, SSHIp = TSSHIp)
#      os.system(Command)          
#      Logit("start-remote")

def FnStartLocalTunnel(TunnleDict:dict):
   TName = TunnleDict["role_name"]
   Tlocal_port = TunnleDict["local_port"]
   TDestinationPort = TunnleDict["destination_port"]   
   print ( Fore.WHITE + "Tunneling Port [ " + Fore.CYAN + TDestinationPort + Fore.WHITE + " ] Server Destination [ " + Fore.CYAN + DestIP + Fore.WHITE + " ] to [ " + Fore.BLUE + Tlocal_port + Fore.WHITE + " ] This Server (Bridge) (" + Fore.BLUE + socket.gethostname() + Fore.WHITE + ") for [ " + Fore.BLUE + TName + Fore.WHITE + " ]" + Style.RESET_ALL )               
   Command = "ssh -NTC -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -f -N -p {SSHPort} {SSHUser}@{SSHIp} -L 0.0.0.0:{local_port}:0.0.0.0:{DestinationPort}"
   Command = Command.format(SSHPort = DestPort, SSHUser = DestUser, SSHIp = DestIP, local_port = Tlocal_port, DestinationPort = TDestinationPort )
   xx = os.system(Command)                                        
   ListofActiveTunel.update({TName:TunnleDict})
   Logit("start-local")

def FnStartRemoteTunnel(TunnleDict:dict):
   TName = TunnleDict["role_name"]   
   Tlocal_port = TunnleDict["local_port"]
   TDestinationPort = TunnleDict["destination_port"]      
   print (Fore.WHITE + "Tunneling Port [ " + Fore.BLUE + Tlocal_port + Fore.WHITE + " ] This Server (UPSTREAM) [ " + Fore.BLUE + socket.gethostname() + Fore.WHITE + " ] to [ " + Fore.CYAN + TDestinationPort + Fore.WHITE + " ] Server Destination (" + Fore.CYAN + DestIP + Fore.WHITE + ") for [ " + Fore.CYAN + TName + Fore.WHITE + " ]" + Style.RESET_ALL )               
   Command = "ssh -R {DestinationPort}:127.0.0.1:{local_port} -N -f -p {SSHPort} {SSHUser}@{SSHIp}"
   Command = Command.format(DestinationPort = TDestinationPort, local_port = Tlocal_port, SSHPort = DestPort, SSHUser = DestUser, SSHIp = DestIP)
   xx = os.system(Command)                                        
   ListofActiveTunel.update({TName:TunnleDict})
   Logit("start-remote")


def GenerateReadyStr():   
   a = len(ListofActiveTunel)
   print("")
   if a > 0:
      for x in ListofActiveTunel:         
         if RunInUpStream:
            _dest = ListofActiveTunel[x]["destination_port"]
            print(f"{_B}{_w}Use This Url [ {Back.GREEN}{_w} {DestIP} {_w}{Back.RESET} ] port [ {Back.GREEN}{_w} {_dest} {Back.RESET}{_w}]{_reset}")
         else:
            _local = ListofActiveTunel[x]["local_port"]
            print(f"{_B}{_w}Use This Url [ {Back.GREEN}{_w} This server IP {_w}{Back.RESET} ] port [ {Back.GREEN}{_w} {_local} {Back.RESET}{_w} ]{_reset}")
   elif len(ListofActiveTunel) == 0:
      print(Style.BRIGHT + Fore.YELLOW + "Tunnel Key Empty")
   else:
      print(Style.BRIGHT + Fore.RED + "Error for tunnel key from json file")


def FnStartTunnle():
   try:
      ListOfTunnel = JsonConfig["tunnel"]
      a = len(ListOfTunnel)
      if a > 0:
         for x in ListOfTunnel:
            if RunInUpStream:
               FnStartRemoteTunnel(x)
            else:
               FnStartLocalTunnel(x)
         GenerateReadyStr()      
      elif len(ListOfTunnel) == 0:
         print(Style.BRIGHT + Fore.YELLOW + "Tunnel Key Empty")
      else:
         print(Style.BRIGHT + Fore.RED + "Error for tunnel key from json file")
   except KeyError:
      print(Style.BRIGHT + Fore.YELLOW + "Tunnel Key Not Found in jsonfile")
   except:
      print(Style.BRIGHT + Fore.YELLOW + "Unknown error in Load Json file")   

   if VarParameterMode is False:   
      FnPrintMenu()

def FnCheckStatusTunnel(sshDict: dict):
   if RunInUpStream is False:      
      str = "{local_port}:0.0.0.0:{DestinationPort}"
      str = str.format(local_port = sshDict["local_port"], DestinationPort = sshDict["destination_port"])               
      TaTunnelType = Style.BRIGHT + "Local" + Style.RESET_ALL      
   else:
      str = "{DestinationPort}:127.0.0.1:{local_port}"   
      str = str.format(local_port = sshDict["local_port"], DestinationPort = sshDict["destination_port"])
      TaTunnelType = Style.BRIGHT + "Remote" + Style.RESET_ALL
   return [TaTunnelType,str]

def FnCheckPID(tunnelRststr: str):
   pids = os.popen("ps ax | grep " + tunnelRststr + " | grep -v grep")                           
   if pids.read() == "":
      return False
   else:
      return True

def FnCheckStatus():
   global ListofActiveTunel
   ListofActiveTunel = {}
   try:
      ListOfTunnel = JsonConfig["tunnel"]
      a = len(ListOfTunnel)
      if a > 0:
         TiTunnelType = Style.BRIGHT + "Tunnel type" + Style.RESET_ALL
         TiTitle = Style.BRIGHT + "Name" + Style.RESET_ALL
         TiIP = Style.BRIGHT + 'IP(Host)' + Style.RESET_ALL
         TiLocalport = Style.BRIGHT + 'Local port' + Style.RESET_ALL
         TiDestPort =  Style.BRIGHT + 'Destination Port' + Style.RESET_ALL
         TiStatus = Style.BRIGHT + 'Status' + Style.RESET_ALL
         print ("")
         print ("{:>5}{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(" ",TiTunnelType, TiTitle, TiIP, TiLocalport, TiDestPort, TiStatus))
         _no = 0
         for x in ListOfTunnel:            
            TName = x["role_name"]            
            Tlocal_port = x["local_port"]
            TDestinationPort = x["destination_port"]            
            SSHIp = DestIP
            tunnelRst = FnCheckStatusTunnel(x)
            if FnCheckPID(tunnelRst[1]) :
               TaStatus = Style.NORMAL + Fore.WHITE + Back.GREEN + "Active" + Style.RESET_ALL               
               ListofActiveTunel.update({TName:x})
            else:
               TaStatus = Style.NORMAL + Fore.WHITE + Back.RED + "Not active" + Style.RESET_ALL
         
            TaTitle = Style.BRIGHT + TName + Style.RESET_ALL
            TaIP = Style.BRIGHT + SSHIp + Style.RESET_ALL
            TaLocalport = Style.BRIGHT + Tlocal_port + Style.RESET_ALL
            TaDestPort =  Style.BRIGHT + TDestinationPort + Style.RESET_ALL
            _no += 1
            print ("{:<5}{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(_no,tunnelRst[0], TaTitle, TaIP, TaLocalport, TaDestPort, TaStatus))
         GenerateReadyStr()   

   except KeyError:
      print(Style.BRIGHT + Fore.YELLOW + "Tunnel Key Not Found in jsonfile")
   except:
      print(Style.BRIGHT + Fore.YELLOW + "Unknown error in Load Json file")         
   if __name__ == "__main__":
      if VarParameterMode is False:   
         FnPrintMenu()

def FnKillProcess(tunnelStr:str):
   try:
      for line in os.popen("ps ax | grep " + tunnelStr + " | grep -v grep"):
         fields = line.split()
         pid = fields[0]                       
         os.kill(int(pid), signal.SIGKILL)                                            
         return True
   except:
      return False

def FnKillAllProcess():
      ActiveSSHTunnel = False
      ListOfTunnel = JsonConfig["tunnel"]
      a = len(ListOfTunnel)
      if a > 0:
         TiTunnelType = Style.BRIGHT + "Tunnel type" + Style.RESET_ALL
         TiTitle = Style.BRIGHT + "Name" + Style.RESET_ALL
         TiIP = Style.BRIGHT + 'IP(Host)' + Style.RESET_ALL
         TiLocalport = Style.BRIGHT + 'Local port' + Style.RESET_ALL
         TiDestPort =  Style.BRIGHT + 'Destination Port' + Style.RESET_ALL
         TiStatus = Style.BRIGHT + 'Action' + Style.RESET_ALL
         print ("")
         print ("{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(TiTunnelType, TiTitle, TiIP, TiLocalport, TiDestPort, TiStatus))
         for x in ListOfTunnel:
            TName = x["role_name"]
            Tlocal_port = x["local_port"]
            TDestinationPort = x["destination_port"]            
            SSHIp = DestIP
            tunnelRst = FnCheckStatusTunnel(x)

            FnCheckPID(tunnelRst[1])
            pids = os.popen("ps ax | grep " + tunnelRst[1] + " | grep -v grep")               
            if pids.read() == "":
               pass
            else:               
               TaStatus = Style.NORMAL + Fore.WHITE + Back.RED + "** KILLED **" + Style.RESET_ALL         
               TaTitle = Style.BRIGHT + TName + Style.RESET_ALL
               TaIP = Style.BRIGHT + SSHIp + Style.RESET_ALL
               TaLocalport = Style.BRIGHT + Tlocal_port + Style.RESET_ALL
               TaDestPort =  Style.BRIGHT + TDestinationPort + Style.RESET_ALL
               print ("{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(tunnelRst[0], TaTitle, TaIP, TaLocalport, TaDestPort, TaStatus))
               ActiveSSHTunnel = True
               if FnKillProcess(tunnelRst[1]):
                  Logit("drop") 
               else:
                  print("")
                  print(f"{Style.BRIGHT + Fore.RED}Fail To kill process ....{Style.RESET_ALL}")
                  print("")
                  Logit("drop-fail") 
               

      if ActiveSSHTunnel is True:         
         pass      
      else:
         print ("")
         print (Style.BRIGHT + Fore.YELLOW +"--------------------" + Style.RESET_ALL)
         print (Style.BRIGHT + Fore.RED +"Active SSH Tunnel Not Found " + Style.RESET_ALL)
         print (Style.BRIGHT + Fore.YELLOW +"--------------------" + Style.RESET_ALL)                  
         Logit("drop-fail")
      if VarParameterMode is False:
         FnPrintMenu() 

def Logit(type):
   global VarParameterMode   
   if __name__ != "__main__":
      VarParameterMode = True      

   if type == "drop":
      FnLogit("KILL", "drop All Active SSH Tunnel","Parameter mode is {}".format(VarParameterMode),"successfully" )         
   elif type == "drop-fail":
      FnLogit("KILL", "drop All Active SSH Tunnel","Parameter mode is {}".format(VarParameterMode),"Fail" )         
   elif type == "start-local":
      FnLogit("START", "Start Local SSH Tunnel","Parameter mode is {}".format(VarParameterMode),"--" )         
   elif type == "start-remote":
      FnLogit("START", "Start Remote SSH Tunnel","Parameter mode is {}".format(VarParameterMode),"--" )         
   elif type == "restart":
      FnLogit("RESTART", "ReStart SSH Tunnel","Parameter mode is {}".format(VarParameterMode),"---" )         

def FnLogit(VactionName,Massege,Mode,Status):
   LogFileName = JsonConfig["logfile"]
   try:
      f = open(LogFileName, "a")
      try:
         now = datetime.now()
         now = now.strftime("%d/%m/%Y %H:%M:%S")
         logs = "\n[ {vDate} ] - [ {vAction} ] - [ {vMode}] -[ {vStatus} ] - [ {vMassege} ]"        
         f.write(logs.format(vDate = now, vAction = VactionName , vMassege = Massege, vMode = Mode, vStatus = Status))
      except:
         print("Something went wrong when writing to the log file [ " + Fore.RED + LogFileName + Fore.RESET + " ]")
      finally:
         f.close()
   except:
      print("Something went wrong when writing to the log file [ " + Style.BRIGHT +  Fore.RED + LogFileName + Style.RESET_ALL + " ]")


def Fnhelp():
   InFo = f"""This program can manage SSH tunnels between two Linux servers, used for bypass limitations in highly restricted networks
 - The information of the tunnels read from a json file with the name `config.json`.
 - Run in tow method
   * Upstream server is {_g}Not Blocked{_w}
     in This method, the Tunnel-Managment software runs on the {_B}{_b}bridge server{_reset}{_w} and the bridge server must be able to connect to the upstream server      

         {bannerlib.GetInfoNetGraph("NormalMode-h")}

     {_w}copy Tunnel-Managment software to the {_B}{_b}Bridge server{_reset}{_w} and set {_B}{_w}'upstream_is_Block'{_reset}{_w} parameter to {_B}{_w}'false'{_reset}{_w} in config file
   
     
     
     
   * Upstream server is {_r}Blocked{_w}
     If access to the {_B}{_c}upstream server{_reset}{_w} is blocked, but this server can connect to the {_B}{_b}bridge server{_reset}{_w}
     in This method, the Tunnel-Managment software runs on the {_B}{_c}Upstream server{_reset}{_w} and this server must be able to connect to the {_B}{_b}bridge server{_reset}{_w}      

         {bannerlib.GetInfoNetGraph("UpstreamMode-h")}

     {_w}copy Tunnel-Managment software to the {_B}{_c}Upstrea server{_reset}{_w} and set {_B}{_w}'upstream_is_Block'{_reset}{_w} parameter to {_B}{_w}'true'{_reset}{_w} in config file
"""
   
   bannerlib.GetInfoNetGraph("NormalMode",BrIP="This Server",UpIP=DestIP)
   

   print(Fore.WHITE + InFo + Style.RESET_ALL)
   print("")
   print(Fore.WHITE + "Run without parameter [ " + Fore.BLUE + "tunnel++" + Fore.WHITE + "    ] for run in UI Mode" + Style.RESET_ALL)
   print(Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -s" + Fore.WHITE + " ] for start All tunnel/s" + Style.RESET_ALL)
   print(Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -u" + Fore.WHITE + " ] for Chek Status of tunnel/s" + Style.RESET_ALL)
   print(Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -d" + Fore.WHITE + " ] for Drop/kill all tunnel/s" + Style.RESET_ALL)
   print(Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -r" + Fore.WHITE + " ] for Restart ( Drop & Start) all tunnel/s" + Style.RESET_ALL)   


def CheckingRootPrivilage():
   user = os.getuid()
   if user != 0:            
      print("")
      print (f"{Style.BRIGHT + Fore.RED}This program requires {Fore.WHITE}root{Fore.RED} privileges.  Run as root using {Fore.WHITE}'sudo'{Fore.RED}.{Style.RESET_ALL}")
      print("")
      return False
   return True

def GetRunMode():
   global RunInUpStream      
   RunInUpStream = lib.GetValue(JsonConfig,"upstream_is_Block")
   if RunInUpStream is False:            
      print(bannerlib.GetModeLabel("NormalMode"))
      print("")
      print(f"{_w}in {_y}Normal Mode{_w} , the SSH-Tunnel-Managment software runs on the {_B}{_b}bridge server{_reset}{_w}")
      print("")
      print(bannerlib.GetInfoNetGraph("NormalMode",BrIP="This Server",UpIP=DestIP))
      print("")      
      print(f"{_w}In this case, the bridge server must be able to connect to the {_b}upstream server{_w}.{_reset}")
      print(f"{_w}If the upstream server is {_r}blocked{_w}, you can Run the SSH-Tunnel-Managment software to the upstream server and change the execution method to the upstream block mode, for mor information {_g}use help{_reset}")
   else:
      print(bannerlib.GetModeLabel("UpstreamMode"))
      print("")
      print(f"{_w}in {_r}UPSREAM BLOCK MODE{_w} , the SSH-Tunnel-Managment software runs on the {_B}{_c}Upstream server{_reset}{_w}")
      print("")
      print(bannerlib.GetInfoNetGraph("UpstreamMode",BrIP="127.0.0.1",UpIP=DestIP))
      print("")
      print(f"{_w}In this case, the Upstream server must be able to connect to the {_c}bridge server{_w}.{_reset}")
   #PrintServerDetail()      

def PrintServerDetail():
   print("")
   print(f"{_w}Destination Server:")      
   print(f" {_w}IP   : {_c}{DestIP}{_reset}")
   print(f" {_w}User : {_c}{DestUser}{_reset}")
   print(f" {_w}Port : {_c}{DestPort}{_reset}")


#################
#################
#################

signal.signal(signal.SIGINT, handler)
FnLoadJsonFile()

RunInUpStream = ""
ListofActiveTunel = {}

if __name__ == "__main__":       
   import lib.BaseFunction as lib
   import lib.banner as bannerlib
   DestIP = JsonConfig['Dest_Server']['ip']
   DestUser = JsonConfig['Dest_Server']['user']
   DestPort = JsonConfig['Dest_Server']['port']

   #_debug = ['-s']
   #sys.argv.extend(_debug)

   
   lib.clearScreen()
   #if CheckingRootPrivilage() is True:
   #   FnExit()

   if len(sys.argv) == 1:
      VarParameterMode = False      
      #FnBanner()
      bannerlib.GetBanner("splash")
      GetRunMode()
      FnPrintMenu()
   elif len(sys.argv) == 2:
      VarParameterMode = True            
      i = sys.argv[1]
      if i.lower() == "-d":          
         bannerlib.GetBanner("splash")
         GetRunMode()
         FnKillAllProcess()
      elif i.lower() == "-u":          
         bannerlib.GetBanner("splash")
         GetRunMode()
         PrintServerDetail()
         FnCheckStatus()
      elif i.lower() == "-s":
         bannerlib.GetBanner("splash")
         GetRunMode()
         print("")
         FnStartTunnle()
      elif i.lower() == "-r":
         Logit("restart")
         bannerlib.GetBanner("splash")
         GetRunMode()
         FnKillAllProcess()          
         FnStartTunnle()
      elif i.lower() == "-h":
         lib.clearScreen()
         bannerlib.GetBanner("splash")
         Fnhelp()
      else:
         print(Style.BRIGHT + Fore.GREEN + "-h" + Fore.WHITE + " for Help")   


