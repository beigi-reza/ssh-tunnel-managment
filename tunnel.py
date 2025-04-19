#! /usr/bin/python3
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import os
import subprocess
import signal
from datetime import datetime, timedelta
import time
import sys
import psutil

current_directory = os.path.dirname(os.path.realpath(__file__))
JsonListFile = os.path.join(current_directory,'conf/config.json')
JsonConfig = lib.BaseFunction.LoadJsonFile(JsonListFile)
SSHKEYFile = lib.BaseFunction.GetValue(JsonConfig,"SSHKEY",verbus=False,ReturnValueForNone='')
SSHKEY = os.path.join(current_directory,'key',SSHKEYFile)
TunnelDict = os.path.join(current_directory,'conf/tunnel.json')
TUNNEL_Json = lib.BaseFunction.LoadJsonFile(JsonFile=TunnelDict,Verbus=False,ReternValueForFileNotFound={})

TUNNEL_LIST = TUNNEL_Json["tunnel"]

_B = "[1m"
_N = "[22m"
_D = "[2m"
_reset = "[0m"
_UN = "\033[4m"
_fw = "[37m"
_fy = "[33m"
_fb = "[34m"
_fbl = "[30m"
_fr = "[31m"
_fc = "[36m"
_fg = "[32m"
_fm = "[35m"
_fEx_w = "[97m"
_fEx_y = "[93m"
_fEx_b = "[94m"
_fEx_bl = "[90m"
_fEx_r = "[91m"
_fEx_c = "[96m"
_fEx_g = "[92m"
_fEx_m = "[95m"


_bw = "[47m"
_by = "[43m"
_bb = "[44m"
_bbl = "[40m"
_br = "[41m"
_bc = "[46m"
_bg = "[42m"
_bm = "[45m"
_brst = "[49m"
_bEx_w = "[107m"
_bEx_y = "[103m"
_bEx_b = "[104m"
_bEx_bl = "[100m"
_bEx_r = "[101m"
_bEx_c = "[106m"
_bEx_g = "[102m"
_bEx_m = "[105m"

if os.path.exists(SSHKEY) == False:
    lib.BaseFunction.clearScreen()
    print('\n\n')
    lib.Logo.sshTunnel()
    lib.AsciArt.BorderIt(Text=f'canot find the SSH key File ({SSHKEY})',BorderColor=_fr,TextColor=_fw)
    lib.BaseFunction.FnExit()


######################################################
######################################################

def MainMenu(Msg = ''):
    while True:        
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        RunWithRoot()
        printTunnelList()                
        if Msg != '':
            print("")
            print("")
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fy,TextColor=_fEx_r)
            Msg = ''
        print(f'\n\n{_fw}( {_fg}s {_fw}) Start all Tunnel{_reset}')
        print(f'{_fw}( {_fr}d {_fw}) Drop all Tunnel{_reset}')
        print(f'{_fw}( {_fr}r {_fw}) Restart all Tunnel{_reset}')
        print(f'{_fw}( . ) Enter tunnel code for more ...{_reset}')
        print(f'\n{_D}q for quit{_reset}')
        UserInput = input(f'{_B}{_fw}Or Enter tunnel Code :  {_reset}')        
        if UserInput.strip().lower() in ['q','s','d','r','']:
            if UserInput == 'q':
                lib.BaseFunction.FnExit()
            elif UserInput == 's':
                StartAllTunnel()
            elif UserInput == 'd':
                DropAllSShTunnel()
            elif UserInput == 'r':
                DropAllSShTunnel()
                StartAllTunnel()
            elif UserInput.strip() == '':
                continue
        else:
            for _ in TUNNEL_LIST:                
                findCode = False
                Msg = ''
                if _["Code"].lower() == UserInput.lower().strip():
                    ViewTunnleStatus(_)
                    findCode = True

            if findCode == False:                
                if Msg == '':
                    Msg = f"No server found ( {UserInput} )"


def ViewTunnleStatus(TunnelDict):
    while True:
        rst = CheckStatusTunnel(TunnelDict)
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()    
        if rst[0]:
            print(f'\nTunnel is : {_fw}{_bg} READY {_reset}')
            print(f"\nTunnel {_fb}{TunnelDict['Name']}{_fw} is running with PID : {_by}{_fbl} {rst[1]} {_reset}")            
            details = GetProcessDetails(rst[1])
        else:
            print(f'\nTunnel is : {_fw}{_bb} STOP {_reset}')
            print(f"\nTunnel {_fw}{TunnelDict['Name']}{_fw} is not running.{_reset}")            
        if {TunnelDict['Type'] == 'local'}:
            LocalOrRemoteServerlable = "Local Server"
        else:
            LocalOrRemoteServerlable = "Remote Server"    

        if TunnelDict["Highly_Restricted_Networks"].get('Enable',False):
            _mode = f'{_by}{_fbl} ENABLED '
        else:
            _mode = f'{_bbl} DISABLED '        
        ModeStr = f'\nHighly restricted network mode : {_mode}{_reset}'
            
        print(f"{ModeStr}")
        print(f"\nTunnel name : {_fc}{TunnelDict['Name']}{_reset}")
        print(f"Tunnel code : {_fc}{TunnelDict['Code']}{_reset}")
        print(f"IP : {_fc}{TunnelDict['ssh_ip']}{_reset}")
        print(f"User : {_fc}{TunnelDict['ssh_user']}{_reset}")
        print(f"Port : {_fc}{TunnelDict['ssh_port']}{_reset}")
        print(f"Final Port on {LocalOrRemoteServerlable} : {_B}{_fc}{TunnelDict['FinalPort']}{_reset}")
        print (f"Advanced Options :")
        print (f"  - Monitor Port : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('MonitorPort',0)}{_reset} Use Only for Highly Restricted Network Mode")
        print (f"  - ServerAliveInterval : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ServerAliveInterval',0)}{_reset}")
        print (f"  - ServerAliveCountMax : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ServerAliveCountMax',0)}{_reset}")
        print (f"  - ExitOnForwardFailure : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure','no')}{_reset}")        

        if rst[0]:
            if details[0]:
                print (f'\n{"-"*30} Process Details {"-"*30}')
                print(f"Process Name : {_fy}{details[1]['name']}{_reset}")                
                print(f"Execute Path : {_fy}{details[1]['exe']}{_reset}")
                print(f"Command Line : {_fy}{details[1]['cmdline']}{_reset}")
                print(f"Status : {_fy}{details[1]['status']}{_reset}")
                print(f"User : {_fy}{details[1]['user']}{_reset}")
                print(f"Memory Info : ")
                print(f"  - RSS : {_fy}{details[1]['memory']['memory_info_RSS']}{_reset}")
                print(f"  - VMS : {_fy}{details[1]['memory']['memory_info_VMS']}{_reset}")
                print(f"Start Time : {_fy}{details[1]['start_time']}{_reset}")
                print(f"CPU Info : ")
                print(f"  - CPU Percent : {_fy}{details[1]['cpu_percent']}{_reset}")
                print(f"  - Parent Process : {_fy}{details[1]['parent']}{_reset}")
                print(f"  - Children Process : {_fy}{details[1]['children']}{_reset}")
                print(f"Network Connections : ")                
                for _conn in details[1]['network']:
                    print(f"  - {_fy}{_conn}{_reset}")
                print (f'\n{"-"*30} Process Details {"-"*30}')                
            else:                                
                print(f'{_fr}Error getting process details.{_reset}')    
                print(details[1])        
        else:
            print (f'\n{"-"*50}')
        if rst[0]:
            print(f'\n{_fw}( {_fr}d {_fw}) for Stop Tunnel.{_reset}')
        else    :
            print(f'\n{_fw}( {_fy}s{_fw} ) for Start Tunnel.{_reset}')    
        print(f'{_fw}( {_fw}Enter {_fw}) for Check Status.{_reset}')
        print(f'{_fw}( {_fc}0 {_fw}) Back to Start Menu.{_reset}')
        print(f'\n{_D}q for quit{_reset}')
        UserInput = input(f'{_B}{_fw}Enter Command :  {_reset}')        
        if UserInput.strip().lower() in ['0','s','q','d']:
            if UserInput == '0':
                if rst[0]:
                    return True
                else:
                    return False
            elif UserInput == 'q':
                lib.BaseFunction.FnExit()
            elif UserInput == 's':
                if rst[0] is False:
                    FnStartTunnel(TunnelDict)
            elif UserInput == 'd':                    
                if rst[0]:
                    KillProcessByPID(rst[1])

def StartAllTunnel():
    for _ in TUNNEL_LIST:
        if CheckStatusTunnel(_)[0]:
            print(f"Tunnel {_['Name']} is already running.")
        else:
            FnStartTunnel(_)

def DropAllSShTunnel():
    for _ in TUNNEL_LIST:                        
        _RST = CheckStatusTunnel(_)
        if _RST[0]:
            KillProcessByPID(_RST[1])


            
def KillProcessByPID(pid,Verbus=False):
    try:        
        pid = int(pid)        
        os.kill(pid, signal.SIGTERM)  # SIGTERM is a graceful termination signal        
        return True
    except ProcessLookupError:
        if Verbus:
            print(f"No process with PID {pid} was found.")
        return False
    except ValueError:
        if Verbus:
            print(f"Invalid PID: {pid}")
        return False
    except PermissionError:
        if Verbus:
            print(f"Permission denied when trying to kill process {pid}.")
        return False
    except Exception as e:
        if Verbus:
            print(f"Error killing process {pid}: {e}")
        return False


#def printTunnelList():
#    TitleStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Name (code)', target_length=20, AlignmentMode='center')}{_reset}"
#    TypeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Type', target_length=10, AlignmentMode='center')}{_reset}"
#    SourceStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Source', target_length=18, AlignmentMode='center')}{_reset}"
#    SSHServerStr = f"{_bb}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='SSH Server', target_length=30, AlignmentMode='center')}{_reset}"
#    FinalPortStr = f"{_by}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Final Port', target_length=30, AlignmentMode='center')}{_reset}"
#    ModeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Mode', target_length=6, AlignmentMode='center')}{_reset}"
#    print(f"\n{ModeStr} {TitleStr} {TypeStr} {SourceStr} {SSHServerStr} {FinalPortStr}\n")
#    for _ in TUNNEL_LIST:
#        a = GenerateTunnelLine(_)
#        print(a)


def printTunnelList():
    for Tunnel in TUNNEL_LIST:    
        _LServer = lib.BaseFunction.GetValue(Tunnel, "Source_Server")
        _LPort = lib.BaseFunction.GetValue(Tunnel, "Source_port")
        _sshPort = lib.BaseFunction.GetValue(Tunnel, "ssh_port")
        _sshIp = lib.BaseFunction.GetValue(Tunnel, "ssh_ip")
        _sshUser = lib.BaseFunction.GetValue(Tunnel, "ssh_user")
        _Type = lib.BaseFunction.GetValue(Tunnel, "Type").upper()
        if _Type == "LOCAL":
            _tColor = _fg
            _FinalIP = lib.BaseFunction.GetLocalIP()        
        elif _Type == "REMOTE":
            _tColor = _fr
            _FinalIP = f'{Tunnel["ssh_ip"]}'
        elif _Type == "DYNAMIC":
            _tColor = _fm
            _FinalIP = f'{Tunnel["ssh_ip"]}'
        else:
            _tColor = _fw
            _FinalIP = ' - '
        _rst = CheckStatusTunnel(Tunnel)
        if _rst[0]:
            _Icon = '▶️'
            _status = 'Running'
            _color = f'{_fEx_y}'
            _FinalPort = f'{_Icon}  {_color}{_FinalIP}:{Tunnel["FinalPort"]}'
            _titelColor = f'{_bg}{_fbl}'
            _StatusColor = f'{_by}{_fbl}'
        else:
            _Icon = '⏸️'
            _status = 'Stopped'
            _FinalPort = f'{_Icon}  {Tunnel["FinalPort"]}'
            _titelColor = f'{_bc}{_fbl}'        
            _StatusColor = f'{_bbl}{_fw}'
        if Tunnel.get('Keep_Alive',False):
            _keppAlive = f'🔒 {_fg}Enabled{_reset}{_D} in keep-alive service{_reset}'
        else:
            _keppAlive = f'🔓 {_D}{_fw}Disabled{_reset}'
        if Tunnel["Highly_Restricted_Networks"].get('Enable',False):
            ModeChr = f'✨ {_D}Highly Restricted Networks{_reset}'
        else:
            ModeChr = f'🔗 {_D}standard {_reset}'
        _Title = f"{Tunnel['Name']}"
        _Code = f"{Tunnel['Code']}"
        
        _SourceOrRemote = f"{_LServer}:{_LPort}"
        _SshServer = f"{_sshUser}@{_sshIp}:{_sshPort}"
        _FinalPort = f"{_FinalPort}"
        _type = f"{_tColor}{_Type}{_reset}"
        sp = ' ' * 10 
        print(f'\n\n{_titelColor}Title      {_reset}:{_titelColor} {_Title}{sp}{_reset}\n')
        print(f'Status     : {_StatusColor} {_status} {_reset} ')
        print(f'Code       : {_fy}{_Code} {_reset} ')
        print(f'Mode       : {ModeChr} ')
        print(f'Keep Alive : {_keppAlive} ')
        print(f'Server     : {_fc}{_SshServer}{_reset} ')
        print(f'Source     : {_fc}{_SourceOrRemote}{_reset} ')
        print(f'Type       : {_type}')
        print(f'Final Port : {_FinalPort}')




        #return f"{_Mode} {_Title} {_type} {_SourceOrRemote} {_SshServer} {_FinalPort}"

#def GenerateTunnelLine(Tunnel):
#    _LServer = lib.BaseFunction.GetValue(Tunnel, "Source_Server")
#    _LPort = lib.BaseFunction.GetValue(Tunnel, "Source_port")
#    _sshPort = lib.BaseFunction.GetValue(Tunnel, "ssh_port")
#    _sshIp = lib.BaseFunction.GetValue(Tunnel, "ssh_ip")
#    _sshUser = lib.BaseFunction.GetValue(Tunnel, "ssh_user")
#    _Type = lib.BaseFunction.GetValue(Tunnel, "Type").upper()
#    if _Type == "LOCAL":
#        _tColor = _fb
#        _FinalIP = lib.BaseFunction.GetLocalIP()        
#    elif _Type == "REMOTE":
#        _tColor = _fc
#        _FinalIP = f'{Tunnel["ssh_ip"]}'
#    elif _Type == "DYNAMIC":
#        _tColor = _fm
#        _FinalIP = f'{Tunnel["ssh_ip"]}'
#    else:
#        _tColor = _fw
#        _FinalIP = ' - '
#    _rst = CheckStatusTunnel(Tunnel)
#    if _rst[0]:
#        _Icon = '▶️'        
#        _FinalPort = f'{_Icon}  {_FinalIP}:{Tunnel["FinalPort"]}'
#        _clPort = f'{_bg}{_fbl}'        
#    else:
#        _Icon = '⏸️'        
#        _FinalPort = f'{_Icon}  {Tunnel["FinalPort"]}'
#        _clPort = f'{_fw}'        
#    if Tunnel.get('Keep_Alive',False):
#        _keppAlive = '🔒'
#    else:
#        _keppAlive = '🔓'
#    if Tunnel["Highly_Restricted_Networks"].get('Enable',False):
#        ModeChr = f'✨ {_keppAlive}'        
#    else:
#        ModeChr = f'🔗 {_keppAlive}'
#    #FullName = f"{Tunnel['Name']} ({_fy}{Tunnel['Code']}{_fw})"
#    FullName = f"{Tunnel['Name']} ({Tunnel['Code']})"
#    _Title = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=FullName, target_length=20, AlignmentMode='left')}{_reset}"
#    _SourceOrRemote = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_LServer}:{_LPort}', target_length=18, AlignmentMode='left')}{_reset}"
#    _SshServer = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_sshUser}@{_sshIp}:{_sshPort}', target_length=30, AlignmentMode='left')}{_reset}"
#    _FinalPort = f"{_clPort}{lib.AsciArt.FnAlignmentStr(originalString=_FinalPort , target_length=30, AlignmentMode='left')}{_reset}"
#    _type = f"{_tColor}{lib.AsciArt.FnAlignmentStr(_Type, target_length=10, AlignmentMode='left')}{_reset}"
#    _Mode = f"{_fy}{lib.AsciArt.FnAlignmentStr(ModeChr, target_length=6, AlignmentMode='left')}{_reset}"
#    return f"{_Mode} {_Title} {_type} {_SourceOrRemote} {_SshServer} {_FinalPort}"


def RunWithRoot():            
    if lib.BaseFunction.User_is_root() is False:
        msg1 = """Tunnel Funcyion requires root privileges, Attempting to restart with sudo..."""
        print('\n\n')
        lib.AsciArt.BorderIt(Text=msg1,BorderColor=_fr,TextColor=_fy,WidthBorder=100)
        print('\n\n')
        #lib.BaseFunction.PressEnterToContinue()
        try:
            # Re-run the script with sudo
            sudo_command = ['sudo', sys.executable] + sys.argv
            subprocess.run(sudo_command, check=True)
        except subprocess.CalledProcessError:
            print("Failed to run with elevated privileges.")
            lib.BaseFunction.FnExit()
            
def CreateCommamd(TunnleDict,TypeOfTunnel):        
    Highly_Restricted_Networks = TunnleDict["Highly_Restricted_Networks"].get('Enable',False)
    if Highly_Restricted_Networks: 
        _sshCommandMode = 'autossh'        
    else:    
        _sshCommandMode = 'ssh'

    if TypeOfTunnel == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Source_Server']}:{TunnleDict['Source_port']}"
    elif TypeOfTunnel == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Source_Server']}:{TunnleDict['Source_port']}"
    elif TypeOfTunnel == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{TunnleDict['FinalPort']}"        
    else:
        print(f"Unknown Tunnel Type: {TypeOfTunnel} for {TunnleDict['Name']}")
        lib.BaseFunction.PressEnterToContinue()
    

    CommandLst = []    

    CommandLst.append(_sshCommandMode)

    if Highly_Restricted_Networks:
        CommandLst.append('-M')
        CommandLst.append(str(TunnleDict["Highly_Restricted_Networks"].get('MonitorPort',0)))
    CommandLst.append('-N')
    CommandLst.append(_SSHType)
    CommandLst.append(_SSHTypeServer)
    CommandLst.append('-p')
    CommandLst.append(str(TunnleDict.get('ssh_port','22')))
    CommandLst.append('-i')
    CommandLst.append(SSHKEY)
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveInterval={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveInterval',0)}")
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveCountMax={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveCountMax',0)}")
    CommandLst.append('-o')
    CommandLst.append(f"ExitOnForwardFailure={TunnleDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure','no')}")
    CommandLst.append(f"{TunnleDict['ssh_user']}@{TunnleDict['ssh_ip']}")
    return CommandLst


def FnStartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())    
    try:
        process = subprocess.Popen(
            Command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,        
            stdin=subprocess.DEVNULL,
            start_new_session=True,            
            )            
        time.sleep(1)        
        _rst = CheckStatusTunnel(TunnleDict)
        if _rst[0]:
            return True,''
        else:
            return False,''
    except Exception as e:
        msg = (f"🔥 Exception occurred while starting autossh: {e}")        
        return  False,msg
    
def FnAutoRestartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())
    while True:        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _LineLog = f"{timestamp},{TunnleDict['Name']},None,Trying to Start Tunnel"
        print (f"{_LineLog}")
        SaveLogWebsite(_LineLog)
        process = subprocess.Popen(
            Command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,        
            stdin=subprocess.DEVNULL,
            start_new_session=False,
            )            
        time.sleep(1)
        _rst = CheckStatusTunnel(TunnleDict)
        Pid = process.pid
        if _rst[0] is False:            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _LineLog = f"{timestamp},{TunnleDict['Name']},{Pid},Error: Unable to start tunnel"
            SaveLogWebsite(_LineLog)
            print (f"{_LineLog}")
            time.sleep(5)
            continue                   
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _LineLog = f"{timestamp},{TunnleDict['Name']},None,Started Tunnel"
            SaveLogWebsite(_LineLog)
            print (f"{_LineLog}")
        while True:
            retcode = process.poll()
            if retcode is not None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
                _LineLog = f"{timestamp},{TunnleDict['Name']},{Pid},Tunnel disconnected! Restarting..."
                SaveLogWebsite(_LineLog)
                print (f"{_LineLog}")        
                break
            time.sleep(5)
        print("waitt for 2 sec")    
        time.sleep(2)

def SaveLogWebsite(LogLine:str ):        
    """آماده سازی لاگ برای ذخیره با فرمت CSV
    به دست آوردن اسم فایل و بررسی وجود

    Args:
        ResponseDict (DICT): Dict of website status.
    """
    RealPath_of_LogFile = os.path.join(current_directory,'logs','KeepAlivelog.csv')    
    if os.path.isfile(RealPath_of_LogFile) is False:
        _Titel = "Time,Name,PID,Msg"
        Saveit(RealPath_of_LogFile,_Titel)        
    Saveit(RealPath_of_LogFile,LogLine)

def Saveit(FileName,Line):    
    """ثبت لاگ دپر فایل

    Args:
        FileName (STR): Realpath of log filwe
        Line (STR): Log for Save To log
    """
    Line = f"{Line}\n"
    try:
        f = open(FileName, "a")
        try:        
            f.write(Line)            
        except:
            print("Something went wrong when writing to the log file [ " + _fr + FileName + _reset + " ]")
        finally:
            f.close()
    except:
        print("Something went wrong when writing to the log file [ " + _B +  _fr + FileName + _reset + " ]")


def CheckStatusTunnel(_Tunnle):
    Highly_Restricted_Networks_mode = _Tunnle["Highly_Restricted_Networks"].get('Enable',False)
    if _Tunnle['Type'] == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Source_Server']}:{_Tunnle['Source_port']}"
    elif _Tunnle['Type'] == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Source_Server']}:{_Tunnle['Source_port']}"
    elif _Tunnle['Type'] == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{_Tunnle['FinalPort']}"        
    
    if Highly_Restricted_Networks_mode:
        CommandStr = 'autossh'
    else:
        CommandStr = 'ssh'

    UserIP = f'{_Tunnle["ssh_user"]}@{_Tunnle["ssh_ip"]}'            
    try:
        # Check if the process exists
        for proc in psutil.process_iter(['cmdline', 'pid', 'name']):
            if proc.name().lower().strip() == CommandStr.lower().strip():                                
                CmdLine = proc.info['cmdline']
                if CmdLine is not None:
                    if UserIP in CmdLine:
                        if _SSHType in CmdLine:
                            if _SSHTypeServer in CmdLine:
                                return True, proc.pid                                    
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False,'error'
    return False,''
    

def CheckAutoSSHCommand():
    """Executes a command and returns its output."""
    command = ['autossh','-V']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True  # Return the output as a string, removing leading/trailing whitespace.
    except subprocess.CalledProcessError as e:        
        return None  # Or raise an exception, depending on your needs.
    except FileNotFoundError:        
        return False
    

def GetProcessDetails(pid):
    """Get detailed information about a process if it exists."""
    details = {}
    try:
        # Check if the process exists
        process = psutil.Process(pid)
        
        # Basic process information
        #print(f"\nPID {pid} found. Process details:")
        #print("=" * 50)
        
        # Process basic info
        try:
            parent = process.parent()
            parentDetails = f"PID {parent.pid} ({parent.name()})"            
        except (psutil.NoSuchProcess, AttributeError):
            parentDetails = 'Not available'

        children = process.children()
        if children:
            for child in children[:5]:  # Limit to first 5 children
                childrenDetail = f"  PID {child.pid} ({child.name()})"                
            if len(children) > 5:                
                childrenDetail = f"  ... and {len(children) - 5} more"
        else:
            childrenDetail = 'None'
        memory_info = process.memory_info()
        create_time = datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        CMDStr = ' '.join(process.cmdline())
        connectionsList = []
        try:            
            #connections = process.net_connections()
            connections = process.connections()
            if connections:                                
                for conn in connections[:5]:  # Limit to first 5 connections
                    local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"                                                                                
                    connectionsList.append(f"  {conn.type} - Local: {local} Remote: {remote} ({conn.status})")
                if len(connections) > 5:
                    connectionsList.append(f"  ... and {len(connections) - 5} more connections")
                    #print(f"  ... and {len(connections) - 5} more connections")
            else:
                connectionsList.append("  None")                
        except (psutil.AccessDenied, psutil.ZombieProcess):            
            connectionsList.append("  Access denied or zombie process")


        details = { 
            'name': process.name(),
            'exe': process.exe(),
            'cmdline': CMDStr,
            'status': process.status(),
            'user': process.username(),
            'memory':{
                'memory_info_RSS': f'{memory_info.rss / (1024 * 1024):.2f} MB',
                'memory_info_VMS': f'{memory_info.vms / (1024 * 1024):.2f} MB'
            },
            'start_time': create_time,
            'cpu_percent': f'{process.cpu_percent(interval=0.1):.1f}%',
            'parent': parentDetails,
            'children': childrenDetail,
            'network': connectionsList
        }
    
        return True, details
        
    except psutil.NoSuchProcess:
        msg = f"PID {pid} not found."
        return False , msg
    except psutil.AccessDenied:
        msg = f"PID {pid} found, but access was denied to get process details."
        return True, msg
    except Exception as e:
        msg = f"An error occurred: {e}"
        return False, msg

def MonitorPortIsUniq():
    """Check if the MonitorPort is unique across all tunnels."""
    MonitorPortlist = []
    for tunnel in TUNNEL_LIST:
        if tunnel["Highly_Restricted_Networks"].get('Enable',False):
            MonitorPort = tunnel["Highly_Restricted_Networks"].get('MonitorPort',0)
            if MonitorPort != 0:
                if MonitorPort in MonitorPortlist:
                    msg = f"MonitorPort {tunnel['Name']}({MonitorPort}) is not unique across tunnels."                    

                    
                MonitorPortlist.append(MonitorPort)

def FnHelp():
    msg = """This program manage SSH tunnels between two Linux servers, run in UI or parameter mode (for scheduled execution). also This solution can be used for all methods for bypass limitations in highly restricted networks.
Refer to the GitHub project documentation to learn how it works."""
    print("")
    lib.AsciArt.BorderIt(Text=msg,WidthBorder=100,BorderColor=_fc,TextColor=_fw)
    print(f"\n{_fw}Syntax:")
    print(f'{_fc}  ./tunnel.py    {_fw}: Run Tunnel Manegment{_reset}')
    print(f'{_fc}  ./tunnel.py -s {_fw}: Start All Tunnel{_reset}')
    print(f'{_fc}  ./tunnel.py -d {_fw}: Drop All Tunnel{_reset}')
    print(f'{_fc}  ./tunnel.py <tunnel code> {_fw}: View Tunnel Status{_reset}\n')
    

             
signal.signal(signal.SIGINT, lib.BaseFunction.handler)

######################################################
######################################################

#_debug = ['en']
#sys.argv.extend(_debug)

if __name__ == "__main__":
    if len(sys.argv) == 1:        
        MainMenu()
    elif len(sys.argv) == 2:        
        _errMsg = False
        if sys.argv[1] in ['-s','--start','--start-all']:
            StartAllTunnel()
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            printTunnelList()
            print('\n')
            lib.BaseFunction.FnExit()
        elif sys.argv[1] in ['-d','--drop','--drop-all']:
            DropAllSShTunnel()
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            printTunnelList()
            print('\n')
            lib.BaseFunction.FnExit()
        elif sys.argv[1] in ['-h','--help']:            
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            FnHelp()
        else:     
            for _ in TUNNEL_LIST:
                if _["Code"].lower().strip() == sys.argv[1].lower().strip():                
                    ViewTunnleStatus(_)
                    _errMsg = True                                
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            print('\n')
            if _errMsg:                
                lib.AsciArt.BorderIt(Text=f"Tunnel Code [ {sys.argv[1]} ] not found.",BorderColor=_fr,TextColor=_fy)
            else:    
                printTunnelList()
    else:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        print(f'\n{_fw}Invalid arguments. Please use [ {_fEx_g}-h{_fw} ] or [ {_fEx_g}--help{_fw} ] for help.{_reset}\n')
        
        


