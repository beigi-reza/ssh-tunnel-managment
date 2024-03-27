from colorama import Fore, Back, Style

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


def GetBanner(name=""):
    if name == "":
        name = "splash"

    if name == "splash":
        print (f"{_D}{_w}  _______                     _   __  __                                              _    {_reset}")
        print (f"{_D}{_w} |__   __|                   | | |  \/  |                                            | |   {_reset}")
        print (f"{_D}{_w}    | |_   _ _ __  _ __   ___| | | \  / | __ _ _ __   __ _  __ _ _ __ ___   ___ _ __ | |_  {_reset}")
        print (f"{_N}{_w}    | | | | | '_ \| '_ \ / _ \ | | |\/| |/ _` | '_ \ / _` |/ _` | '_ ` _ \ / _ \ '_ \| __| {_reset}")
        print (f"{_N}{_w}    | | |_| | | | | | | |  __/ | | |  | | (_| | | | | (_| | (_| | | | | | |  __/ | | | |_  {_reset}")
        print (f"{_B}{_w}    |_|\__,_|_| |_|_| |_|\___|_| |_|  |_|\__,_|_| |_|\__,_|\__, |_| |_| |_|\___|_| |_|\__| {_reset}")
        print (f"{_B}{_w}                                                            __/ |                          {_reset}")
        print (f"{_B}{_w}                                                           |___/                           {_reset}")

def GetInfoNetGraph(name:str,UpIP="",BrIP=""):
    if UpIP != "":
        BrIP = "Bridge Server (" + BrIP + ")"
    else:
        BrIP = "Bridge Server"

    if UpIP != "": 
        UpIP = "UpStream Server (" + UpIP + ")"
    else:
        UpIP = "UpStream Server"
    _InfoGraph = ""
    if name == "NormalMode":
        _InfoGraph = f"(( {_B}{_w}User {_g}<-->{Back.RED}{_w} {BrIP}{_reset} {_g}<-->{_c} {UpIP} {_g} <-->{_w} Free Internet )){_reset}"
    elif name == "UpstreamMode":        
        _InfoGraph = f"(( {_B}{_w}User {_g}<-->{_b} {BrIP} {_g}<--{_r}x {Back.RED}{_w} {UpIP}{_reset} {_g} <-->{_w} Free Internet )){_reset}"
    elif name == "UpstreamMode-h":
        _InfoGraph = f"(( {_B}{_w}User {_g}<-->{_b} {BrIP} {_g}<--{_r}x{_c} {UpIP} {_g} <-->{_w} Free Internet )){_reset}"
    elif name == "NormalMode-h":        
        _InfoGraph = f"(( {_B}{_w}User {_g}<-->{_b} {BrIP} {_g}<-->{_c} {UpIP} {_g} <-->{_w} Free Internet )){_reset}"
    return _InfoGraph

def GetModeLabel(name:str):
    _label = ""
    if name == "NormalMode":
        _label = f"{Back.WHITE}{_b}   NORMAL  MODE   {_reset}"
    elif name == "UpstreamMode":
         _label = f"{Back.RED}{_w}   UPSREAM BLOCK MODE   {_reset}"
    return _label