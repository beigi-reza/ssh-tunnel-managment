#####################################################
# Fn_CenterString
# Update GetValue - 1403-09-03
from colorama import Fore, Back, Style




def FnAlignmentStr(originalString: str, target_length: int, padding_char: str = " ",AlignmentMode = "center") -> str:
    """اضافه کردن و بزرگ کردن رشته دریافتی و برگشت آن به طول درخواستی

    Args:
        originalString (str): متن اصلی
        target_length (int): طول رشته نهایی
        padding_char (str, optional): عبارتی که افزایش طول عبارت با آن صورت پذیرد
        AlignmentMode (str, optional): مارجین متن در عبارت

    Returns:
        str: _description_
    """
    if len(originalString) >= target_length:
        return originalString 
        
    total_padding = target_length - len(originalString)
    if AlignmentMode not in ['center','left','right']:
        Aligment = 'left'
    if AlignmentMode.lower() == 'center':        
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        _str =  padding_char * left_padding + originalString + padding_char * right_padding
    elif AlignmentMode.lower() == 'left':
        total_padding = total_padding - 1
        _str = padding_char + originalString + padding_char * total_padding
    elif AlignmentMode.lower() == 'right':
        total_padding = total_padding - 1
        _str = padding_char * total_padding + originalString + padding_char
    return _str

def wrap_text(text, max_width=100):
    """
    Wraps the given text to a specified maximum width.

    Args:
        text: The input text to be wrapped.
        max_width: The maximum width of each line.

    Returns:
        A list of lines, where each line has a maximum width of max_width.
    """

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > max_width:  # Add 1 for the space
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line += word + " "
    
    if current_line.strip():
        lines.append(current_line.strip())
    return lines



def BorderIt(Text:str,BorderColor = '',TextColor = '', WidthBorder = 100):
    """ Create a Border in Text
    Args:
        Text (str): Input text
        BorderColor (str, optional): Border Color_. Defaults to 'WHITE'.
        TextColor (str, optional): TextColor. Defaults to 'WHITE'.
        WidthBorder (int, optional): Width of Box. Defaults to 100.
    """
    if TextColor == '':
        TextColor = Fore.WHITE
    if BorderColor == '':
        BorderColor = Fore.WHITE

    LenStr = len(Text) + 2
    if LenStr > WidthBorder:
        LenStr = WidthBorder         
    RowLine = '─' * LenStr
    Upline = BorderColor + f'┌{RowLine}┐' + Style.RESET_ALL
    Dwonline = BorderColor + f'└{RowLine}┘' + Style.RESET_ALL
    ClmnChar = f'{BorderColor}│{Style.RESET_ALL}'
    lines = wrap_text(text=Text,max_width=WidthBorder - 1)
    print(Upline)
    for line in lines:
        if LenStr == WidthBorder:
            aa = len(line)
            a = WidthBorder - len(line) - 1
            space_al = ' ' * a
        else:
            space_al = ' '    
        print(f'{ClmnChar} {TextColor}{line}{space_al}{ClmnChar}')
    print(Dwonline)



if __name__ == "__main__":    
    print(f"{Style.NORMAL + Fore.YELLOW}You should not run this file directly")
