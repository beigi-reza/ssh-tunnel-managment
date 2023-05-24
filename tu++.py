#! /usr/bin/python3
from colorama import Fore, Back, Style
from datetime import datetime
import sys
import os
import json
import signal

JsFilePath = "<JSPATH>/config.json"


def FnBanner():
    print (Fore.BLUE + "    ______  ______                       __        ______   " + Fore.RESET)
    print (Fore.CYAN + "   / / / / /_  __/_  ______  ____  ___  / / __    _\ \ \ \  " + Fore.RESET)
    print (Fore.GREEN + "  / / / /   / / / / / / __ \/ __ \/ _ \/ /_/ /___/ /\ \ \ \ " + Fore.RESET)
    print (Fore.RED + "  \ \ \ \  / / / /_/ / / / / / / /  __/ /_  __/_  __/ / / / " + Fore.RESET)
    print (Fore.YELLOW + "   \_\_\_\/_/  \__,_/_/ /_/_/ /_/\___/_/ /_/   /_/ /_/_/_/  " + Fore.RESET)
    print (Fore.MAGENTA + "                                                            " + Fore.RESET)

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
       FnCheckStatus()
    elif usrInput.lower() == "s":   
       FnStartTunnle()
    elif usrInput.lower() == "d":      
       FnKillProcess()
    elif usrInput.lower() == "q":      
      sys.exit()
    elif usrInput.lower() == "h":
       print("")
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



def FnStartTunnle():
#   ListOfTunnel = JsonConfig["tunnel"]
   try:
      ListOfTunnel = JsonConfig["tunnel"]
      a = len(ListOfTunnel)
      if a > 0:
         for x in ListOfTunnel:
            TName = x["role_name"]
            Tlocal_port = x["local_port"]
            TDestinationPort = x["destination_port"]
            Ttype = x["type"]
            TSSHIp = x["ssh_ip"]
            TSSHPort = x["ssh_port"]
            TSSHUser = x["ssh_user"]
            if Ttype == "local":
               print (Style.BRIGHT + Fore.WHITE + "Tunneling Port [ " + Fore.RED + TDestinationPort + Fore.WHITE + " ] Server [ " + Fore.RED + TSSHIp + Fore.WHITE + " ] to [ " + Fore.RED + Tlocal_port + Fore.WHITE + " ] server Local for [ " + Fore.BLUE + TName + Fore.WHITE + " ]" + Style.RESET_ALL )               
               Command = "sudo ssh -NTC -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -f -N -p {SSHPort} {SSHUser}@{SSHIp} -L 0.0.0.0:{local_port}:0.0.0.0:{DestinationPort}"
               Command = Command.format(SSHPort = TSSHPort, SSHUser = TSSHUser, SSHIp = TSSHIp, local_port = Tlocal_port, DestinationPort = TDestinationPort )
               os.system(Command)                                        
               Logit("start-local")
            elif Ttype == "remote":               
               print (Style.BRIGHT + Fore.WHITE + "Remote Tunneling port [ " + Fore.RED + Tlocal_port + Fore.WHITE + " ] local server to server [ " + Fore.RED + TSSHIp + Fore.WHITE + " ] port [ " + Fore.RED + TDestinationPort + Fore.WHITE + " ] for [ " + Fore.BLUE + TName + " ] " + Style.RESET_ALL)
               Command = "ssh -R 0.0.0.0:{DestinationPort}:127.0.0.1:{local_port} -N -f -p {SSHPort} {SSHUser}@{SSHIp}"
               Command = Command.format(DestinationPort = TDestinationPort, local_port = Tlocal_port, SSHPort = TSSHPort, SSHUser = TSSHUser, SSHIp = TSSHIp)
               os.system(Command)          
               Logit("start-remote")
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


def FnCheckStatus():
   try:
      ListOfTunnel = JsonConfig["tunnel"]
      a = len(ListOfTunnel)
      if a > 0:
         TiTunnelType = Style.BRIGHT + "Tunnel type" + Style.RESET_ALL
         TiTitle = Style.BRIGHT + "Title" + Style.RESET_ALL
         TiIP = Style.BRIGHT + 'IP(Host)' + Style.RESET_ALL
         TiLocalport = Style.BRIGHT + 'Local port' + Style.RESET_ALL
         TiDestPort =  Style.BRIGHT + 'Destination Port' + Style.RESET_ALL
         TiStatus = Style.BRIGHT + 'Status' + Style.RESET_ALL
         print ("")
         print ("{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(TiTunnelType, TiTitle, TiIP, TiLocalport, TiDestPort, TiStatus))
         for x in ListOfTunnel:
            TName = x["role_name"]
            Tlocal_port = x["local_port"]
            TDestinationPort = x["destination_port"]
            Ttype = x["type"]
            SSHIp = x["ssh_ip"]
            if Ttype == "local":
               #str = "0.0.0.0:{local_port}:0.0.0.0:{DestinationPort}"
               str = "{local_port}:0.0.0.0:{DestinationPort}"
               str = str.format(local_port = Tlocal_port, DestinationPort = TDestinationPort)               
               TaTunnelType = Style.BRIGHT + "Local" + Style.RESET_ALL
            elif Ttype == "remote":
               str = "0.0.0.0:{DestinationPort}:127.0.0.1:{local_port}"
               str = str.format(local_port = Tlocal_port, DestinationPort = TDestinationPort)
               TaTunnelType = Style.BRIGHT + "Remote" + Style.RESET_ALL

            pids = os.popen("ps ax | grep " + str + " | grep -v grep")               
            if pids.read() == "":
                TaStatus = Style.NORMAL + Fore.WHITE + Back.RED + "Not active" + Style.RESET_ALL
            else:
               TaStatus = Style.NORMAL + Fore.WHITE + Back.GREEN + "Active" + Style.RESET_ALL
         
            TaTitle = Style.BRIGHT + TName + Style.RESET_ALL
            TaIP = Style.BRIGHT + SSHIp + Style.RESET_ALL
            TaLocalport = Style.BRIGHT + Tlocal_port + Style.RESET_ALL
            TaDestPort =  Style.BRIGHT + TDestinationPort + Style.RESET_ALL
            print ("{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(TaTunnelType, TaTitle, TaIP, TaLocalport, TaDestPort, TaStatus))

   except KeyError:
      print(Style.BRIGHT + Fore.YELLOW + "Tunnel Key Not Found in jsonfile")
   except:
      print(Style.BRIGHT + Fore.YELLOW + "Unknown error in Load Json file")         
   if VarParameterMode is False:   
      FnPrintMenu()

def FnKillProcess():
      ActiveSSHTunnel = False
      ListOfTunnel = JsonConfig["tunnel"]
      a = len(ListOfTunnel)
      if a > 0:
         TiTunnelType = Style.BRIGHT + "Tunnel type" + Style.RESET_ALL
         TiTitle = Style.BRIGHT + "Title" + Style.RESET_ALL
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
            Ttype = x["type"]
            SSHIp = x["ssh_ip"]
            if Ttype == "local":
               #str = "0.0.0.0:{local_port}:0.0.0.0:{DestinationPort}"
               str = "{local_port}:0.0.0.0:{DestinationPort}"
               str = str.format(local_port = Tlocal_port, DestinationPort = TDestinationPort)               
               TaTunnelType = Style.BRIGHT + "Local" + Style.RESET_ALL
            elif Ttype == "remote":
               str = "0.0.0.0:{DestinationPort}:127.0.0.1:{local_port}"
               str = str.format(local_port = Tlocal_port, DestinationPort = TDestinationPort)
               TaTunnelType = Style.BRIGHT + "Remote" + Style.RESET_ALL

            pids = os.popen("ps ax | grep " + str + " | grep -v grep")               
            if pids.read() == "":
                pass
            else:               
               TaStatus = Style.NORMAL + Fore.WHITE + Back.RED + "** KILLED **" + Style.RESET_ALL         
               TaTitle = Style.BRIGHT + TName + Style.RESET_ALL
               TaIP = Style.BRIGHT + SSHIp + Style.RESET_ALL
               TaLocalport = Style.BRIGHT + Tlocal_port + Style.RESET_ALL
               TaDestPort =  Style.BRIGHT + TDestinationPort + Style.RESET_ALL
               print ("{:<20} {:<30} {:<20} {:<20} {:<30} {:<15}".format(TaTunnelType, TaTitle, TaIP, TaLocalport, TaDestPort, TaStatus))
               ActiveSSHTunnel = True
               try:
                   for line in os.popen("ps ax | grep " + str + " | grep -v grep"):
                       fields = line.split()
                       pid = fields[0]                       
                       os.kill(int(pid), signal.SIGKILL)                       
               except:
                   pass                             
               Logit("drop") 

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
   InFo = """ This program can manage SSH tunnels between two Linux servers.
   The information of the tunnels read from a json file.
   This program can be run in UI and parameter mode (for scheduled execution)."""

   print(Style.BRIGHT + Fore.WHITE + InFo + Style.RESET_ALL)
   print("")
   print(Style.BRIGHT + Fore.WHITE + "Run without parameter [ " + Fore.BLUE + "tunnel++" + Fore.WHITE + "    ] for run in UI Mode" + Style.RESET_ALL)
   print(Style.BRIGHT + Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -s" + Fore.WHITE + " ] for start All tunnel/s" + Style.RESET_ALL)
   print(Style.BRIGHT + Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -u" + Fore.WHITE + " ] for Chek Status of tunnel/s" + Style.RESET_ALL)
   print(Style.BRIGHT + Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -d" + Fore.WHITE + " ] for Drop/kill all tunnel/s" + Style.RESET_ALL)
   print(Style.BRIGHT + Fore.WHITE + "Run with parameter    [ " + Fore.BLUE + "tunnel++ -r" + Fore.WHITE + " ] for Restart ( Drop & Start) all tunnel/s" + Style.RESET_ALL)   


if len(sys.argv) == 1:   
   VarParameterMode = False
   FnLoadJsonFile()
   FnBanner()
   FnPrintMenu()
else:
   VarParameterMode = True
   FnLoadJsonFile()
   for i in sys.argv:
       if i.lower() == "-d":          
          FnBanner()
          FnKillProcess()
       elif i.lower() == "-u":          
          FnBanner()
          FnCheckStatus()
       elif i.lower() == "-s":
          FnBanner()
          FnStartTunnle()
       elif i.lower() == "-r":
          Logit("restart")
          FnBanner()
          FnKillProcess()          
          FnStartTunnle()
       elif i.lower() == "-h":
          FnBanner()
          Fnhelp()
       else:
          print(Style.BRIGHT + Fore.GREEN + "-h" + Fore.WHITE + " for Help")   
          
   
