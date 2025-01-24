from symbol_map import *
from editor_renderer import *
import sys

def handle_command_mode(editor, key):
    if key == "ENTER":
        editor.mode = "normal"
        execute(editor.command_buffer, editor)
        editor.command_buffer = ""
    elif key == "BACKSPACE":
        editor.command_buffer = editor.command_buffer[:-1]
    elif key == "ESCAPE":
        editor.mode = "normal"
        editor.command_buffer = ""
    else: 
        editor.type_command_char(key)

def execute(command, editor):
    if command.startswith("w"):
        write_file(editor)
    elif command.startswith("q"):
        editor.quit = True
        exit_enviroment()
        sys.exit()
    elif command.startswith("wq"):
        write_file(editor)
        editor.quit = True
        exit_enviroment()
        sys.exit()
    elif command.startswith("q!"):
        editor.quit = True
        exit_enviroment()
        sys.exit()
    else:
        editor.status_message = "Unknown command"
