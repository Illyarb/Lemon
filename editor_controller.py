from expression import Atom, Summation, Matrix
from tui import *
class Cursor:
    def __init__(self, x,y):
        self.x = x
        self.y = y

class EditorController:
    def __init__(self):
        self.mode = "normal"
        self.cursor = Cursor(0,0)
        self.lines = [Atom(""), Summation("i=0", "2", "i + 2"),Atom(""),Atom(""),Atom(""), Matrix(2,2,[["1","2"],["3","4"]])]
        # self.lines = [Atom("x²"),Summation("i=0", "2", "i + 2")]
# ,Summation("i=0", "2", "i + 2")]
        self.vbuffer = ""
        self.command_buffer = ""
        self.line_heights = []
        self.focused_line = 0
        for i in self.lines:
            self.line_heights.append(i.height)

    def get_current_line(self):
        return self.lines[self.focused_line]

    def render(self):
        clear_screen()
        draw_footer(self)
        height_offset = 0
        for no, line in enumerate(self.lines):
            line.isFocused = no == self.focused_line
            move_cursor(0, no + height_offset)
            line_stry = gray(str(no)) if no != self.focused_line else pink(str(no))
            putstr(line_stry + " ")
            move_cursor(3, no + height_offset)
            line.render()
            height_offset += line.height

    def new_line(self):
        self.lines.insert(self.focused_line + 1, Atom(""))
        self.focused_line += 1

    def type_command_char(self, key):
        self.command_buffer += key


    def delete_line(self):
        if self.focused_line == 0:
            self.lines.pop(0)
            self.lines.insert(0, Atom(""))
            return

        self.lines.pop(self.focused_line)
        self.focused_line -= 1

    def check_vbuffer(self):
        if self.vbuffer.endswith("sum"):
            pass

    def type(self, key):
        self.get_current_line().type_char(key)
        self.vbuffer += key
        self.cursor.x += 1

    def backspace(self):
        self.get_current_line().backspace()

    def go_left(self):
        if self.cursor.x == 0:
            return
        self.cursor.x -= 1
        self.get_current_line().go_left()

    def go_right(self):
        self.cursor.x += 1
        self.get_current_line().go_right()

    def go_up(self):
        self.get_current_line().go_up()

    def go_down(self):
        self.get_current_line().go_down()

    def go_up_line(self):
        # if self.cursor.y == 0:
        #     return
        # self.cursor.y -= 1
        if self.focused_line == 0:
            return
        self.focused_line -= 1

    def go_down_line(self):
        # if self.cursor.y == len(self.lines) - 1:
        #     return
        # self.cursor.y += 1
        if self.focused_line == len(self.lines) - 1:
            return
        self.focused_line += 1

    def quit(self):
        self.quit = True

    def write_file(self):
        pass
    

