from editor_renderer import *
from editor_controller import EditorController
from commands import *
import sys
import tty
import termios
from tui import *

vbuffer = ""
def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if key == '\x7f':
                key = 'BACKSPACE'
            elif key == '\r':
                key = 'ENTER'
            elif key == '\x1b':
                key = 'ESCAPE'
            elif key == '\x1b[A':
                key = 'UP'
            elif key == '\x1b[B':
                key = 'DOWN'
            elif key == '\x1b[C':
                key = 'RIGHT'
            elif key == '\x1b[D':
                key = 'LEFT'
            elif key == '\x1b[3~':
                key = 'DELETE'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


def handle_visual_mode(editor, key):
    pass

def handle_insert_mode(editor, key):
    if key == " ":
        return
    if key == "ESCAPE":
        editor.mode = "normal"
        return 
    if key == "ENTER":
        editor.new_line()
        return
    if key == "BACKSPACE":
        editor.backspace()
        return 

    editor.type(key)

def handle_normal_mode(editor, key):
    if key == 'i':
        editor.mode = "insert"
    # if key == "q":
    #     exit_enviroment()
    #     sys.exit()
    if key == "ENTER":
        editor.mode = "navigation"
    if key == "i":
        editor.mode = "insert"
    if key == "j":
        editor.go_down_line()
    if key == "k":
        editor.go_up_line()
    if key == "l":
        editor.mode = "navigation"
    if key == "h":
        editor.mode = "navigation"
    if key == ":":
        editor.mode = "command"

    if key == "d":
        global vbuffer
        if vbuffer == "":
            vbuffer = "d"
            return 
        
        if vbuffer == "d":
            editor.delete_line()
            vbuffer = ""

def handle_navigation_mode(editor, key):
    if key == "h":
        editor.go_left()
    if key == "l":
        editor.go_right()
    if key == "ESCAPE":
        editor.mode = "normal"



def main():
    editor = EditorController()
    enter_enviroment()
    while True:
        editor.render()
        key = get_key()
        if editor.mode == "normal":
            handle_normal_mode(editor, key)
            continue
        if editor.mode == "insert":
            handle_insert_mode(editor, key)
            continue
        if editor.mode == "navigation":
            handle_navigation_mode(editor, key)
            continue
        if editor.mode == "command":
            handle_command_mode(editor, key)
            continue

if __name__ == '__main__':
    main()

