import lib.BaseFunction
import lib.AsciArt

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


SourceAddress = ''
DestinationPort = ''


def CreateNewTunnelMenu():
    while True:        
        msg = f'{_B}{_fw}\n Create New Tunnel [ Local / Remote / Dynamic ]{_reset}'
        userInput = input(f'{msg} {_N}{_fy} [ L / R / D ] {_N}{_fw} > {_N}')
        if userInput.lower().strip() in ['l','local']:
            return 'local'
        elif userInput.lower().strip() in ['r','remote']:
            return 'remote'
        elif userInput.lower().strip() in ['d','dynamic']:
            return 'dynamic'


def tunnleProgress(ServerDict = None ,Mode = 'local',GetValue = None):
    NC = f'{_bw}{_fbl}'
    SelecteingColor = f'{_by}{_fbl}'    
    SelecttedColor = f'{_bg}{_fbl}'
    DC = f'{_B}{_fw}'
    S_Clr = NC
    D_clr = NC

    if GetValue == 'source_address':        
        S_Clr = SelecteingColor
    elif GetValue == 'final_port':                
        S_Clr = SelecttedColor
        D_clr = SelecteingColor
    elif GetValue == 'confirm':
        S_Clr = SelecttedColor
        D_clr = SelecttedColor

    if SourceAddress == '':
        SourceStr = f'Source Address'
    else:
        SourceStr = SourceAddress

    if DestinationPort == '':
        _DestStr = f'Final Port'        
    else:
        _DestStr = DestinationPort
    



    SShServeraddr = f'{ServerDict["User"]}@{ServerDict["IP"]}:{ServerDict["Port"]}'
    S_SrvStr = f"{lib.AsciArt.FnAlignmentStr(originalString = f'🔌 {SourceStr}',target_length=20)}"
    SShAdr = f"{lib.AsciArt.FnAlignmentStr(originalString = f'🔑  {SShServeraddr}',target_length=30)}"
    FinalPortTitle = f"{lib.AsciArt.FnAlignmentStr(originalString = f'🏁 {_DestStr}',target_length=12)}"
    ThisPc = f"{lib.AsciArt.FnAlignmentStr(originalString = '💻 This computer',target_length=18)}"
    
    FirewallStr = f'🔥 Firewall'
    R_Aro = f'➡'        
        

    LineUp = '┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'
    LineDown = '└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘'

    
    if Mode == 'local':        
        TitleStr = f' {S_Clr}{S_SrvStr}{_reset} {R_Aro} {DC}{SShAdr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset}: {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'remote':
        TitleStr = f' {DC}{ThisPc}{_reset}{R_Aro} {S_Clr}{S_SrvStr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{SShAdr}{_reset} : {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'dynamic':    
        TitleStr = f' {S_Clr}{S_SrvStr}{_reset} {R_Aro} {DC}{SShAdr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset}'        
    print(f'{_fy}{LineUp}{_reset}')
    if Mode == 'dynamic':
        _sp = ' ' * 19
    else:
        _sp = ' ' * 3    
    print(f'{_fy}│ {_reset}{TitleStr}{_sp}{_fy}│{_reset}')    
    print(f'{_fy}{LineDown}{_reset}')

def TunnelHelp(Color = _fy):
    print('\n')
    TunnelHelpMode(Mode = 'local',ColorBox = Color)
    TunnelHelpMode(Mode = 'remote',ColorBox = Color)
    TunnelHelpMode(Mode = 'dynamic',ColorBox = Color)
    print('')
def TunnelHelpMode(Mode = 'local',ColorBox = _fy):

    FirewallStr = f'🔥 Firewall'
    R_Aro = f'➡'        
    SourceStr = f'🔌 Source Address '
    SShServr = f'🔑 SSH Server'
    FinalPortTitle = f'🏁 Final Port'
    ThisPc = f'🖥️  This Server '
    DC = f'{_B}{_fw}'
    S_Clr = f'{_B}{_fw}'
    D_clr = f'{_B}{_fw}'


    if Mode == 'local':        
        TitleStr = f' {S_Clr}{SourceStr}{_reset}{R_Aro} {DC}{SShServr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset} {R_Aro} {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'remote':
        TitleStr = f' {DC}{ThisPc}{_reset}{R_Aro} {S_Clr}{SourceStr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{SShServr}{_reset} {R_Aro} {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'dynamic':    
        TitleStr = f' {S_Clr}{SourceStr}{_reset} {R_Aro} {DC}{SShServr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset}'        

    LineUp = '┌─────────────────────────────────────────────────────────────────────────────────────┐'
    LineDown = '└─────────────────────────────────────────────────────────────────────────────────────┘'

    ModeTitle = lib.AsciArt.FnAlignmentStr(originalString = f'{Mode.upper()} >', target_length = 13)
    if Mode == 'dynamic':
        _sp = ' ' * 17
    else:
        _sp = ' '
    print(f'{" "*13}{ColorBox}{LineUp}{_reset}')
    print(f'{ColorBox}{ModeTitle}│ {_reset}{TitleStr}{ColorBox}{_sp}│{_reset}')    
    print(f'{" "*13}{ColorBox}{LineDown}{_reset}')


def getSourceAddress(msg = ''):
    global SourceAddress
    SourceAddress = ''
    while True:
        if msg != '':
            print(f'\n{_N}{_fw} {msg}{_reset}')
            msg = ''

        UserInput = input(f'{_B}{_fw}\nEnter 🔌  {_fy}Source Address{_fw} [ {_fy}IP:Port{_fw} / {_fy}Port{_fw} ] > {_reset}')
        if UserInput.strip() == '':
            continue
        else:
            if ':' in UserInput:
                ip,port = UserInput.split(':')
                if lib.BaseFunction.FnIsValidIP(ip) or ip.lower().strip() == 'localhost':
                    if port.isdigit() and len(port) < 6 and len(port) > 0 and int(port) > 0 and int(port) < 65535:
                        SourceAddress = UserInput.strip()
                        return SourceAddress
                else:
                    msg = f'{_fr}Invalid IP or Port{_reset}'
            else:
                try:
                    if int(UserInput.strip()) > 0 and int(UserInput.strip()) < 65535:
                        SourceAddress = f'localhost:{UserInput.strip()}'                        
                        return SourceAddress
                    else:
                        msg = f'{_fr}Invalid Port{_reset}'    
                except:                        
                    msg = f'{_fr}Invalid IP or Port{_reset}'
                

def GetFinalport(msg = ''):
    global DestinationPort
    DestinationPort = ''
    while True:
        if msg != '':
            print(f'\n{_N}{_fw} {msg}{_reset}')
            msg = ''
        UserInput = input(f'{_B}{_fw}\nEnter 🏁 {_fy}Final Port{_fw} [ {_fy}Port{_fw} ] > {_reset}')
        if UserInput.strip() == '':
            continue
        else:
            try:
                if int(UserInput.strip()) > 0 and int(UserInput.strip()) < 65535:
                    DestinationPort = UserInput.strip()
                    return DestinationPort
                else:
                    msg = f'{_fr}Invalid Port{_reset}'
            except:                        
                msg = f'{_fr}Invalid Port{_reset}'


def Createtunnel(msg = ''):
    while True:
        if msg != '':
            print(f'\n{_N}{_fw} {msg}{_reset}')
            msg = ''
        UserInput = input(f'{_B}{_fw}\nConfirm{_fw} [ Yes / Save / No ] {_fy}[ Y / S / N ]{_fw} > {_reset}')
        if UserInput.lower().strip() in ['yes','y','']:
            return True,'run'
        elif UserInput.lower().strip() in ['s','save']:
            return True,'save'            
        else:
            if UserInput.lower().strip() in ['n','no']:
                return False,''
            else:
                msg = f'{_fr}Invalid Input{_reset}'

if __name__ == "__main__":        
    print(f"{_B}{_fy}You should not run this file directly")
