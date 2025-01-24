import sys
from base64 import standard_b64encode
import os   
from symbol_map import var_map, op_map, special_map, other_map
from PIL import Image
from image_processing import generate_tight_symbol
from io import BytesIO
from itertools import product

cursor_x = 0
cursor_y = 0
sum_image = generate_tight_symbol(symbol="∑", fontsize=100)
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

def putstr(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def clear_screen():
    sys.stdout.write("\033[2J")
    sys.stdout.flush()

def move_cursor(x, y):
    global cursor_x, cursor_y
    cursor_x = x
    cursor_y = y
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

def enter_alt_screen():
    sys.stdout.write("\033[?1049h")
    sys.stdout.flush()

def exit_alt_screen():
    sys.stdout.write("\033[?1049l")
    sys.stdout.flush()

def echo_off():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def echo_on():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def set_cursor_visible():
    print("\033[?25h")

def set_cursor_invisible():
    print("\033[?25l")

def get_terminal_size():
    return os.get_terminal_size()

def enter_enviroment():
    enter_alt_screen()
    echo_off()
    set_cursor_invisible()

def exit_enviroment():
    exit_alt_screen()
    echo_on()
    set_cursor_visible()

def move_cursor_right(n):
    move_cursor(cursor_x + n, cursor_y)

def move_cursor_left(n):
    move_cursor(cursor_x - n, cursor_y)

def move_cursor_up(n):
    move_cursor(cursor_x, cursor_y - n)

def move_cursor_down(n):
    move_cursor(cursor_x, cursor_y + n)


def clear_images():
    sys.stdout.write("\033_Ga=d,d=A\033\\")
    sys.stdout.flush()

def get_cursor_position():
    global cursor_x, cursor_y
    return cursor_x, cursor_y

def display_image(pillow_image, rows=None, cols=None):

    cursor_x, cursor_y = get_cursor_position()
    # Convert image to PNG and base64 encode
    image_buffer = BytesIO()
    pillow_image.save(image_buffer, format="PNG")
    image_data = standard_b64encode(image_buffer.getvalue()).decode("ascii")
    
    # First, position the cursor
    sys.stdout.write(f"\033[{cursor_y + 1};{cursor_x + 1}H")
    sys.stdout.flush()

    # Send the image data in chunks
    pos = 0
    chunk_size = 4096
    
    while pos < len(image_data):
        chunk = image_data[pos:pos + chunk_size]
        more = 1 if pos + chunk_size < len(image_data) else 0
        
        if pos == 0:
            # First chunk includes placement info
            cmd = "\033_Gf=100,a=T"  # Transmit and show
            if rows is not None:
                cmd += f",r={rows}"
            if cols is not None:
                cmd += f",c={cols}"
            cmd += f",m={more};{chunk}\033\\"
        else:
            # Subsequent chunks only need more flag
            cmd = f"\033_Gm={more};{chunk}\033\\"
        
        sys.stdout.write(cmd)
        sys.stdout.flush()
        pos += chunk_size

    # Ensure we end with a newline to maintain terminal state
    sys.stdout.write("\n")
    sys.stdout.flush()

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
    if editor.mode == "command":
        print(":" + editor.command_buffer)

