#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
# Update GetValue - 1403-09-03

import json
from tabnanny import verbose
from colorama import Fore, Back, Style
from datetime import datetime
import sys
import os
from os import system, name
from time import sleep
import shutil
import socket


#######################################################
_B = Style.BRIGHT
_N = Style.NORMAL
_D = Style.DIM
_w = Fore.WHITE
_y = Fore.YELLOW
_b = Fore.BLUE
_r = Fore.RED
_c = Fore.CYAN
_g = Fore.GREEN
_bl = Fore.BLACK
_lb = Fore.LIGHTBLUE_EX 
_lc = Fore.LIGHTCYAN_EX
_ly = Fore.LIGHTYELLOW_EX
_lr = Fore.LIGHTRED_EX
_reset = Style.RESET_ALL
_Br = Back.RED
_Bb = Back.BLUE
_By = Back.YELLOW + Fore.WHITE
_Bg = Back.GREEN
_Bw = Back.WHITE
#######################################################


def clearScreen():
    # for windows
    if name == 'nt':
        _ = system('cls')
        print("ted")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


## Load Json File and return it as Dictionary
def LoadJsonFile(JsonFile,Verbus = True,ReternValueForFileNotFound = None): 
    try:
        JsFile = open(JsonFile, "r")
    except:
        if Verbus:
            print(Style.BRIGHT + Fore.RED + "Json File Not Found [ " + Fore.WHITE + JsonFile + Fore.RED + " ] " + Style.RESET_ALL)            
            sys.exit()
        else:
            return ReternValueForFileNotFound
          
            
    js = JsFile.read()
    js  = js.replace('\n', '') 
    global JsonConfig   
    return json.loads(js)


def FnCreateDirectory(your_directory:str,Verbus = True):
  try:
    if not os.path.exists(your_directory):
      os.makedirs(your_directory)
      return True
  except FileExistsError:
    if Verbus:
      print(f"Directories '{your_directory}' already exist.")
    return False  
  except OSError as e:
    if Verbus:
      print(f"Error creating directories '{your_directory}': {e}")
    return False  

def CheckExistDir(YourPath:str,Title_dir='',Verbus = False):
  """Check Exist Dir.
  Args:
    Path: Path of Folder
    Title: Title for file for Promt
    PrintIt: Verbus
  Returns:
    The equivalent number of seconds.
  """
  if os.path.isdir(YourPath) is False:
      if Verbus is True:                 
          print(f"{_B}{_w}The path {Title_dir} [{_lr} {YourPath} {_w} ] not exists")
          print(f'{_B}{_w}If the path is correct, for create run this Comand [ {_c} mkdir -p {YourPath} ] {_reset}')          
      return False  
  else:
      return True

def isFile(Path:str,Title : str ,Verbus = True):
  """ Check Exist File.
  Args:
    Path : path of file
    Title : Titel of file
    PrintIt : True or False
  Return: 
      return True or False
  """
  if os.path.isfile(Path) is True:
    return True
  else:
    if Verbus is True:       
       print(Style.BRIGHT + Fore.WHITE + Title + "File [ " + Style.BRIGHT + Fore.LIGHTRED_EX + Path + Fore.WHITE + Style.BRIGHT +" ] Not found " + Style.RESET_ALL)                        
    return False

def IsExist(path,FileOrDir='',title='',Verbus=False):
  if os.path.exists(path) is True:
    return True
  else:
    if FileOrDir.lower() == "file":
       if Verbus is True:
          print(Style.BRIGHT + Fore.WHITE + title + "File [ " + Style.BRIGHT + Fore.LIGHTRED_EX + path + Fore.WHITE + Style.BRIGHT +" ] Not found " + Style.RESET_ALL)                        
       return False
    elif FileOrDir.lower() == "folder":
       if Verbus is True:
          print(Style.BRIGHT + Fore.WHITE +  title + " [ " + Style.BRIGHT + Fore.LIGHTRED_EX + path + Fore.WHITE + Style.BRIGHT +" ] not exists " + Style.RESET_ALL)                     
       return False
    elif FileOrDir.lower() == "dir":
       if Verbus is True:       
          print(Style.BRIGHT + Fore.WHITE +  title + " [ " + Style.BRIGHT + Fore.LIGHTRED_EX + path + Fore.WHITE + Style.BRIGHT +" ] not exists " + Style.RESET_ALL)                     
          print(Style.BRIGHT + Fore.WHITE + "If the path is correct, for create run this Comand [ " + Fore.CYAN + "mkdir -p {}".format(path) + Fore.WHITE + " ] " + Style.RESET_ALL )
       return False

def GetValue(InputDict:dict,*Key,verbus = True,ReturnValueForNone = None,TerminateApp = False):
  """برای خواندن مقداری از یک دیکشنری همراه با مدیریت خطاها و مقدار برگشتی.

  Args:
    InputDict: دبکشنری ورودی
    Key: مفداری که جستجو برای آن انجامخواهد و تا 5 زیر مرحله را قبول می کند
    verbus: در صورت پیدا نشدن مقدار پیغام دهد 
    ReturnValueForNone:  در صپرت پیدا نشدن مقدار این متغیر برگردانده می شود . مقدار پیشفرض نان
    TerminateApp : اگر مقدار بگیرد از نرم افزار خارج می شود
  Returns:
    مقدار متغیر دریافتی در صورت وجود    
  Example:
    GetValue(jsonConfig,"DockerMode") 
    GetValue(jsonConfig,"DockerMode","container_name")
    GetValue(jsonConfig,"section1","section2","section3")
    GetValue(jsonConfig,"DockerMode","container_name","xc",verbus=False)
    GetValue(jsonConfig,"DockerMode","container_name","xc",verbus=False,ReturnValueForNone='')
  """
  ValueNotFoun = False
  if len(Key) == 1:
    try:
      Value = InputDict[Key[0]]              
    except:
      ValueNotFoun = True
  elif len(Key) == 2:
    try:
      Value = InputDict[Key[0]][Key[1]]      
    except:
      ValueNotFoun = True
  elif len(Key) == 3:
    try:
      Value = InputDict[Key[0]][Key[1]][Key[2]]
    except:
      ValueNotFoun = True  
  elif len(Key) == 4:
    try:       
      Value = InputDict[Key[0]][Key[1]][Key[2]][Key[3]]
    except:
      ValueNotFoun = True  
  elif len(Key) == 5:
    try:       
      Value = InputDict[Key[0]][Key[1]][Key[2]][Key[3]][Key[4]]
    except:
      ValueNotFoun = True  
  elif len(Key) == 6:
    try:       
      Value = InputDict[Key[0]][Key[1]][Key[2]][Key[3]][Key[4]][Key[5]]
    except:
      ValueNotFoun = True  

  if ValueNotFoun:  
    if verbus:
      Rst = ''
      for _ in Key:
        Rst = Rst + f'["{_}"]'
      #print(Style.BRIGHT + Back.RED+ Fore.WHITE + "Value (({})) Not Found / GetValue Function in BaseFunction.py".format(Rst) + Style.RESET_ALL)
      print(f'{_B}{_w}Value  {_r}{Rst}{_w}   Not Found . {_reset}/ GetValue Function in BaseFunction.py')
      input(Style.BRIGHT + Fore.WHITE + "Press Any Key to ... ")      
      if TerminateApp:
        FnExit()
    return ReturnValueForNone            
  return Value


def GetJsonObject(InputJsonConfig,jsonkey,ObjectType):      
  try:
    a = InputJsonConfig[jsonkey]
    if ObjectType == "str":
       ReturnObj = ""
       ReturnObj = a
       return ReturnObj
    elif ObjectType == "list":
      Returnlist = []
      Returnlist = list(a)
      return Returnlist
    elif ObjectType == "dic":
      Returndic = {} 
      Returndic = a.copy()     
      return Returndic    
    elif ObjectType == "bool":
      Returndic = False
      Returndic = a
      return Returndic        
    else:
      print("ObjectTypeInvalid In FnGetJsonObject()")
    
  except KeyError:    
    if ObjectType == "str":
      ReturnObj = ""      
      return ReturnObj
    elif ObjectType == "list":
      Returnlist = []
      return Returnlist
    elif ObjectType == "dic":
      Returndic = {}      
      return Returndic
    else:
      print("ObjectTypeInvalid In FnGetJsonObject()")
  
def logit(LogFileName,action,message):
    #LogFileName = JsonConfig["LogPath"] +"/BackupWP-"+ Now + ".logs"
    try:
      f = open(LogFileName, "a")
      try:
        DateAndTime = datetime.now()
        DateAndTime = DateAndTime.strftime("%d/%m/%Y %H:%M:%S")        
        logs = f"[{DateAndTime}] - [{action}] - [{message}]\n"
        f.write(logs)        
      except:
        print("Something went wrong when writing to the log file [ " + Fore.RED + LogFileName + Fore.RESET + " ]")
      finally:
        f.close()
    except:
      print("Something went wrong when writing to the log file [ " + Style.BRIGHT +  Fore.RED + LogFileName + Style.RESET_ALL + " ]")

def ChekSizeFile(FileName,WaitTime):    
    """check size of file after wait time
  
    Args:
        FileName : Str : Path of File
        WaitTime ( int ) : Time to wait for check file size
  
    Returns:
        if file size not change return True else False
    """
    FileStats = os.stat(FileName)
    FileSize1 = FileStats.st_size
    sleep(WaitTime)
    FileStats = os.stat(FileName)
    FileSize2 = FileStats.st_size
    if FileSize1 == FileSize2:
       return True
    else:
       return False

def DeleteFileOrDir(path,verbus = True):  
  Resualt = ""
  if os.path.exists(path):
    if os.path.isfile(path):       
       try:
         os.remove(path)         
         if verbus is True:
            print(Fore.WHITE + Style.BRIGHT + "Remove file [ " + Fore.RED + path + Fore.WHITE +" ]" + Style.RESET_ALL)
         return [True,""]       
       except FileNotFoundError:
         if verbus is True:
            print(Fore.RED + Style.BRIGHT + "File not found [ " + Fore.WHITE + path + Fore.RED + " ]" + Style.RESET_ALL )         
         return [False,"File not found"]
       except PermissionError:
         if verbus is True:
            print(Fore.RED + Style.BRIGHT + "Permission denied for Delete file [ " + Fore.WHITE + path + Fore.RED + " ]" + Style.RESET_ALL)
         return [False,"Permission denied for Delete file"]
       except:
         if verbus is True:
            print("Something went wrong to Delele file [{}]".format(path))                  
         return [False,"Something went wrong to Delele file"]                                                             
    elif os.path.isdir(path):       
       try:
         shutil.rmtree(path)
         if verbus is True:
            print(Fore.WHITE + Style.BRIGHT + "Remove Direcory [ " + Fore.RED + path + Fore.WHITE +" ]" + Style.RESET_ALL)                
         return [True,""]         
       except FileNotFoundError:
         if verbus is True:
            print("Directory not found [{}]".format(path))
         return [False,"Directory not found"]
       except PermissionError:         
         if verbus is True:
            print(Fore.RED + Style.BRIGHT + "Permission denied for Delete file [ " + Fore.WHITE + path + Fore.RED + " ]" + Style.RESET_ALL)         
         return [False,"Permission denied for Delete file"]
       except:         
         if verbus is True:
            print("Something went wrong to Delele Directory [{}]".format(path))         
         return [False,"Something went wrong to Delele Directory"]
  else:
    if verbus is True:
        print("File or directory [ {} ] Not Found".format(path))
    return [False,"File or directory nof found"]

def CheckErrorNumScp(ErrorNo):
   if ErrorNo == 0:
      return ""
   elif ErrorNo == 256:
      return "File or Directory Not Found"
   else:
      return "Unknow Error"
      
def Now():  
  Now = datetime.now()
  Now = Now.strftime("%Y-%m-%d_%H-%M-%S")
  return Now

#def GetColor(ColourDict:dict,ColourName:str,STRING:str):
#  try:
#    Value = ColourDict[ColourName]        
#  except:    
#    Value = {'fore': '', 'back': '', 'style': ''}
#  #  
#  ForeColour = ""
#  BackColour = ""
#  StyleColour = ""
#  UnderLineTxt = False
#  #
#
#  try:
#    x = Value["uberline"]    
#  except:
#    x = False
#
#  if type(x) == bool:
#    UnderLineTxt = x
#  if type(x) == str:
#    if x.lower() == "yes":
#      UnderLineTxt = True
#    elif x.lower() == "true":
#      UnderLineTxt = True
#    else:  
#      UnderLineTxt = False
#  
#  if Value["fore"].upper() == "WHITE":
#    ForeColour=Fore.WHITE
#  elif Value["fore"].upper() == "CYAN":
#    ForeColour=Fore.CYAN
#  elif Value["fore"].upper() == "BLACK":
#    ForeColour=Fore.BLACK
#  elif Value["fore"].upper() == "BLUE":
#    ForeColour=Fore.BLUE
#  elif Value["fore"].upper() == "GREEN":
#    ForeColour=Fore.GREEN
#  elif Value["fore"].upper() == "RED":
#    ForeColour=Fore.RED
#  elif Value["fore"].upper() == "MAGENTA":
#    ForeColour=Fore.MAGENTA
#  elif Value["fore"].upper() == "YELLOW":
#    ForeColour=Fore.YELLOW
#  elif Value["fore"].upper() == "LIGHTBLACK":
#    ForeColour=Fore.LIGHTBLACK_EX
#  elif Value["fore"].upper() == "LIGHTYELLOW":
#    ForeColour=Fore.LIGHTYELLOW_EX
#  elif Value["fore"].upper() == "LIGHTBLUE":
#    ForeColour=Fore.LIGHTBLUE_EX
#  elif Value["fore"].upper() == "LIGHTCYAN":
#    ForeColour=Fore.LIGHTCYAN_EX
#  elif Value["fore"].upper() == "LIGHTGREEN":
#    ForeColour=Fore.LIGHTGREEN_EX
#  elif Value["fore"].upper() == "LIGHTMAGENTA":
#    ForeColour=Fore.LIGHTMAGENTA_EX
#  elif Value["fore"].upper() == "LIGHTRED":
#    ForeColour=Fore.LIGHTRED_EX
#  elif Value["fore"].upper() == "LIGHTWHITE":
#    ForeColour=Fore.LIGHTWHITE_EX
#  else:
#    ForeColour=Fore.WHITE
#
#  if Value["back"].upper() == "BLACK":
#    BackColour = Back.BLACK
#  if Value["back"].upper() == "LIGHTBLACK":
#    BackColour = Back.LIGHTBLACK_EX
#  elif Value["back"].upper() == "BLUE":
#    BackColour = Back.BLUE
#  elif Value["back"].upper() == "LIGHTBLUE":
#    BackColour = Back.LIGHTBLUE_EX    
#  elif Value["back"].upper() == "CYAN":
#    BackColour = Back.CYAN
#  elif Value["back"].upper() == "LIGHTCYAN":
#    BackColour = Back.LIGHTCYAN_EX
#  elif Value["back"].upper() == "GREEN":
#    BackColour = Back.GREEN
#  elif Value["back"].upper() == "LIGHTGREEN":
#    BackColour = Back.LIGHTGREEN_EX    
#  elif Value["back"].upper() == "MAGENTA":
#    BackColour = Back.MAGENTA
#  elif Value["back"].upper() == "LIGHTMAGENTA":
#    BackColour = Back.LIGHTMAGENTA_EX
#  elif Value["back"].upper() == "RED":
#    BackColour = Back.RED
#  elif Value["back"].upper() == "LIGHTRED":
#    BackColour = Back.LIGHTRED_EX
#  elif Value["back"].upper() == "WHITE":
#    BackColour = Back.WHITE
#  elif Value["back"].upper() == "LIGHTWHITE":
#    BackColour = Back.LIGHTWHITE_EX
#  elif Value["back"].upper() == "YELLOW":
#    BackColour = Back.YELLOW
#  elif Value["back"].upper() == "LIGHTYELLOW":
#    BackColour = Back.LIGHTYELLOW_EX
#  else:
#    BackColour = ""
#  
#  if Value["style"].upper() == "NORMAL":
#    StyleColour = Style.NORMAL
#  elif Value["style"].upper() == "BOLD":
#    StyleColour = Style.BRIGHT
#  elif Value["style"].upper() == "DIM":
#    StyleColour = Style.DIM
#  elif Value["style"].upper() == "":  
#    StyleColour = Style.NORMAL
#  else:
#    StyleColour = Style.DIM
#  
#  if BackColour == "":
#    txt = StyleColour + ForeColour + STRING + Style.RESET_ALL
#  else:
#    txt = StyleColour + BackColour + ForeColour + STRING + Style.RESET_ALL  
#
  ## Set Underline
def AddUnderline(Text):
    StartCharachter = "\033[4m"
    EndCharachter = "\033[0m"
    return StartCharachter + Text + EndCharachter

def AddBlink(Text):
    StartCharachter = "\033[32;5m"
    EndCharachter = "\033[0m"
    return StartCharachter + Text + EndCharachter

def fnPrintMenuNavigation(Title1 = "",Title2 = "",Title3 = "",Title4 = "" ):
    StartNavigationBarWith  = "  > "
    EndNavigationBarWith = " |"
    Separator = " -> "
    HilightColor = Style.NORMAL + Fore.YELLOW
    NormalColor = Style.DIM + Fore.YELLOW    
    #
    ResetColor = Style.RESET_ALL
    MainText = HilightColor + "Main Menu" + ResetColor
    FinalMenuStr = MainText

    if Title1 != "":
        MainText = NormalColor + "Main Menu" + ResetColor
        T1 = HilightColor + Title1 + ResetColor
        FinalMenuStr = MainText + Separator + T1

    if Title2 != "":
        T1 = NormalColor + Title1 + ResetColor
        T2 = HilightColor + Title2 + ResetColor
        FinalMenuStr = MainText + Separator + T1 + Separator + T2
    
    if Title3 != "":
        T1 = NormalColor + Title1 + ResetColor
        T2 = NormalColor + Title2 + ResetColor
        T3 = HilightColor + Title3 + ResetColor
        FinalMenuStr = MainText + Separator + T1 + Separator + T2 + Separator + T3
    
    if Title4 != "":
        T1 = NormalColor + Title1 + ResetColor
        T2 = NormalColor + Title2 + ResetColor
        T3 = NormalColor + Title3 + ResetColor
        T4 = HilightColor + Title4 + ResetColor
        FinalMenuStr = MainText + Separator + T1 + Separator + T2 + Separator + T3 + Separator + T4

    print("")
    print(StartNavigationBarWith + FinalMenuStr + EndNavigationBarWith)
    print("")

def handler(signum, frame):
    print("")
    print(Style.NORMAL + Fore.RED + " Force Exit By press [ " + Fore.WHITE + "CTRL + C" + Fore.RED + " ]")
    print("")
    FnExit(ErrorCode=0)

def PrintMessage(messageString : str,MsgType="notif",BackgroudMsg = True,TreminateApp = False,AddLine = True,addSpace = 2,CustomColor= ''):
    """Converts seconds to minutes.
    Args:
      messageString: String Of message
      MsgType : ('error,'warning','notif','msg' or '' for CustomColor)
      BackgroudMsg: True or False For Backgroud Color (defualt is true)
      TreminateApp: True or False For Terminate App after Message
      AddLine: True or False for Add line To Top and button Msg
      addSpace: Nummeric : Add Space begin of msg
      CustomColor: CustomColor Code
    Returns:
      Generate Nsg and Print It
    Example:
    PrintMessage(messageString="Test Msg ...")
    PrintMessage(messageString="Test Msg ...", MsgType="error")
    PrintMessage(messageString="Test Msg ...", MsgType="error", AddLine = True)
    PrintMessage(messageString="Test Msg ...", MsgType="error", AddLine = True, addSpace = 3)
    PrintMessage(messageString="Test Msg ...", MsgType="error", AddLine = True, addSpace = 3)  
    """

    beginSpace = ''
    if MsgType.lower() == 'error':
      if BackgroudMsg:
        BodyColor = _Br + _B + _w
      else:
        BodyColor = _B + _r      
    elif MsgType.lower() == 'warning':
      if BackgroudMsg:
        BodyColor = _By + _B
      else:
        BodyColor = _B + _y  
    elif MsgType.lower() == 'notif':      
      if BackgroudMsg:
        BodyColor = _Bb + _B + _w
      else:
        BodyColor = _B + _b
    elif MsgType.lower() == 'msg':      
      if BackgroudMsg:
        BodyColor = _Bw + _B + _bl
      else:
        BodyColor = _B + _w
    
    if CustomColor.strip() != '':
      BodyColor = CustomColor
      
    if addSpace > 0 :
      beginSpace = ' '
      for _sp in range(addSpace):
        beginSpace = beginSpace + ' '

    print("")
    _line  = f"{beginSpace}{_B}{_w}----------------------------------{_reset}" 
    if AddLine:      
      print(_line)
    print( beginSpace + BodyColor + messageString + Style.RESET_ALL)
    if AddLine:  
      print(_line)
      print("")    
    if TreminateApp: 
      sys.exit()    

def FnExit(Msg="",ErrorCode = 0):
    if Msg != "":                        
        print(f'\n\n{_r}{Msg}{_reset}')             
    sys.exit(ErrorCode)

def convert_seconds_to_minutes(seconds):
    """Converts seconds to minutes.
    Args:
        seconds: An integer representing the number of seconds.
    Returns:
        A tuple containing the number of minutes and the remaining seconds.
        ex: minutes, remaining_seconds = convert_seconds_to_minutes(seconds)
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return minutes, remaining_seconds

def milliseconds_to_seconds(milliseconds):
  """Converts milliseconds to seconds.

  Args:
    milliseconds: The number of milliseconds to convert.

  Returns:
    The equivalent number of seconds.
  """
  return int(milliseconds / 1000)

#####
#FnExit(Msg='test test',Backgroud=False,MsgType='notif')

def ensure_trailing_slash(path):
  """اطمینان از وجود اسلاش در انتهای آدرس ها.
  Args:
    path: The input path.
  Returns:
    The path with a trailing slash.
  """
  if not path.endswith(os.path.sep):
    path += os.path.sep
  return path

def PressEnterToContinue(message="Press Enter to continue..."):
    """Displays a message and waits for the user to press Enter."""
    print(message, end="", flush=True)  # Print message without newline and flush output buffer
    input()
    print()
    
def delete_all(directory,DeleteOnlyDirectory = False):
    """تمام فایل ها و زیر شاخه های موجود در یک میسر مشخص را حذف می کند.
      محدودیت هایی برای عدم حذف شاخه های اصلی سیستم عامل ایجاد شده است
    Args:
      directory: The path to the directory to be deleted.
      DeleteOnlyDirectory : Only Delete Directoties.
    """
    
    IgnorList = ["","bin","boot","etc","dev","home","opt","proc","root","run","sys","var"]  
    for _ignore in IgnorList:
        if f"/{_ignore}" == directory:        
          return False
        
    for root, dirs, files in os.walk(directory, topdown=False):
      if DeleteOnlyDirectory is False:
          for file in files:
              os.remove(os.path.join(root, file))
      for dir in dirs:      
        shutil.rmtree(os.path.join(root, dir))
    return True  

def FindString(string, substring,CaseSensitivity = False):
  """
    Finds the starting index of a substring within a string.

  Args:
      string: The string to search in.
      substring: The substring to search for.

  Returns:
      True or False
  """
  if CaseSensitivity is False:
      string = string.lower()
      substring = substring.lower()
    
  index  = string.find(substring)
  if index != -1:
      return True
  else:
      return False

def User_is_root():
  """Checks if the current user is root (superuser) on Unix-like systems.

  Returns:
    True if the user is root, False otherwise.
  """
  return os.geteuid() == 0

def GetLocalIP(Verbus = False):
    try:
        # Create a socket connection to an external server
        # This doesn't actually establish a connection but helps determine which network interface would be used
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use Google's public DNS server
        s.connect(("8.8.8.8", 80))
        # Get the local IP address
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        if Verbus:
            print (f"Error determining local IP: {e}")
        return None



if __name__ == "__main__":    
  print(f"{Style.NORMAL + Fore.YELLOW}You should not run this file directly")
  a = {}
  