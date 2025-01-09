import sys
from base64 import standard_b64encode
import os   
from symbol_map import var_map, op_map, special_map, other_map
#Display image using Kitty's terminal graphics protocol
def display_image(cursor_x, cursor_y, image_path):

    try:
        with open(image_path, "rb") as img_file:
            image_data = standard_b64encode(img_file.read()).decode("ascii")
        sys.stdout.write(f"\033[{cursor_y + 1};{cursor_x + 1}H")
        sys.stdout.flush()
        pos = 0
        chunk_size = 4096
        while pos < len(image_data):
            more = 1 if pos + chunk_size < len(image_data) else 0

            if pos == 0:
                escape_sequence = (
                    f"\033_Gf=100,a=T,m={more};{image_data[pos:pos+chunk_size]}\033\\"
                )
            else:
                escape_sequence = (
                    f"\033_Gm={more};{image_data[pos:pos+chunk_size]}\033\\"
                )

            sys.stdout.write(escape_sequence)
            sys.stdout.flush()

            pos += chunk_size

    except FileNotFoundError:
        print(f"Error: File not found - {image_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

def render_editor(editor):
    clear_screen()
    draw_footer(editor)
    move_cursor(0,0)
    for no, line in enumerate(editor.lines):
        render_line(line,editor, no)

def get_render_line_string(linestr):
    linestr = linestr.replace(" ", "")
    for symbol, unicode_char in var_map.items():
        linestr = linestr.replace(symbol, cyan(unicode_char)) 
    for symbol, unicode_char in op_map.items():
        linestr = linestr.replace(symbol, orange(unicode_char)) 
    for symbol, unicode_char in special_map.items():
        linestr = linestr.replace(symbol, red(unicode_char))
    for symbol, unicode_char in other_map.items():
        linestr = linestr.replace(symbol, unicode_char)
    return linestr

def render_line(line, editor, no):
    if editor.cursor.y == no:
        linestr = line.get_cursor_string()
    else:
        linestr = line.get_string()

    linestr = get_render_line_string(linestr)
    print(gray(str(no)) + " " + linestr)


def get_terimainl_size():
    return os.get_terminal_size()
def gray(text):
    return f"\033[90m{text}\033[0m"

def cyan(text):
    return f"\033[36m{text}\033[0m"

def green(text):
    return f"\033[32m{text}\033[0m"

def orange(text):
    return f"\033[38;5;215m{text}\033[0m"

def pink(text):
    return f"\033[38;5;212m{text}\033[0m"

def purple(text):
    return f"\033[35m{text}\033[0m"

def red(text):
    return f"\033[31m{text}\033[0m"

def yellow(text):
    return f"\033[33m{text}\033[0m"

# Background versions
def bg_gray(text):
    return f"\033[100m{text}\033[0m"

def bg_cyan(text):
    return f"\033[46m{text}\033[0m"

def bg_green(text):
    return f"\033[42m{text}\033[0m"

def bg_orange(text):
    return f"\033[48;5;215m{text}\033[0m"

def bg_pink(text):
    return f"\033[48;5;212m{text}\033[0m"

def bg_purple(text):
    return f"\033[45m{text}\033[0m"

def bg_red(text):
    return f"\033[41m{text}\033[0m"

def bg_yellow(text):
    return f"\033[43m{text}\033[0m"

def bg_light_gray(text):

    return f"\033[7m\033[K{text}\033[0m"


def clear_screen():
    print("\033[H\033[J")
def move_cursor(x,y):
    print(f"\033[{y};{x}H")
def enter_alt_screen():
    print("\033[?1049h")
def exit_alt_screen():
    print("\033[?1049l")
def echo_off():
    print("\033[?25l")
def echo_on():
    print("\033[?25h")
def set_cursor_visible():
    print("\033[?25h")
def set_cursor_invisible():
    print("\033[?25l")
def get_terminal_size():
    return os.get_terminal_size()

def draw_footer(editor):
    line = editor.get_current_line()
    terminal_size = get_terminal_size()
    move_cursor(0, terminal_size.lines)
    if editor.mode == "normal":
        print(bg_green(str(editor.mode)))
    if editor.mode == "insert":
        print(bg_pink(str(editor.mode)))
    if editor.mode == "navigation":
        print(bg_red(str(editor.mode)))



def enter_enviroment():
    enter_alt_screen()
    echo_off()
    set_cursor_invisible()

def exit_enviroment():
    exit_alt_screen()
    echo_on()
    set_cursor_visible()


