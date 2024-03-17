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


def GetBanner(name:str):
    if name == "splash":
        print ("  _______                     _   __  __                                              _    ")
        print (" |__   __|                   | | |  \/  |                                            | |   ")
        print ("    | |_   _ _ __  _ __   ___| | | \  / | __ _ _ __   __ _  __ _ _ __ ___   ___ _ __ | |_  ")
        print ("    | | | | | '_ \| '_ \ / _ \ | | |\/| |/ _` | '_ \ / _` |/ _` | '_ ` _ \ / _ \ '_ \| __| ")
        print ("    | | |_| | | | | | | |  __/ | | |  | | (_| | | | | (_| | (_| | | | | | |  __/ | | | |_  ")
        print ("    |_|\__,_|_| |_|_| |_|\___|_| |_|  |_|\__,_|_| |_|\__,_|\__, |_| |_| |_|\___|_| |_|\__| ")
        print ("                                                            __/ |                          ")
        print ("                                                           |___/                           ")


def PrintNetGraph(name:str,UpIP="",BrIP=""):        
    BrIP = "Bridge Server (" + BrIP + ")"
    UpIP = "UpStream Server (" + UpIP + ")"
    if name == "NormalMode":
        print(f"{Back.WHITE}{_b}   NORMAL  MODE   {_reset}")
        print("")
        print(f"(( {_B}{_w}User {_g}-->{_b} {BrIP} {_g}-->{_c} {UpIP} {_g} -->{_w} Free Internet{_reset} ))")         
    elif name == "UpstreamMode":
        print(f"{Back.RED}{_w}   UPSREAM BLOCK MODE   {_reset}")
        print("")
        print(f"(( {_B}{_w}User {_g}-->{_b} {BrIP} {_g}<--{_c} {UpIP} {_g} -->{_w} Free Internet{_reset} ))")         
    elif name == "BlockMode":
        print("")
        print(f"(( {_B}{_w}User {_g}-->{_b} {BrIP} {_r}--x{_c} {UpIP} {_g} -->{_w} Free Internet{_reset} ))")         
        print("")

