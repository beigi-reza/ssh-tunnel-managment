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


COLOR_LIST = ['_fw','_fy','_fb','_fbl','_fr','_fc','_fg','_fm','_fEx_w','_fEx_y','_fEx_b','_fEx_bl','_fEx_r','_fEx_c','_fEx_g','_fEx_m']
#########################
##########################

def sshTunnel(Mode=1):
    if Mode == 1:
        print(f'{_D}{_fc} _____ _____ _____    _____                 _ {_reset}')
        print(f'{_D}{_fc}|   __|   __|  |  |  |_   _|_ _ ___ ___ ___| |{_reset}')
        print(f'{_N}{_fc}|__   |__   |     |    | | | | |   |   | -_| |{_reset}')
        print(f'{_B}{_fc}|_____|_____|__|__|    |_| |___|_|_|_|_|___|_|{_reset}')
if __name__ == "__main__":        
    print(f"{_B}{_fy}You should not run this file directly")


