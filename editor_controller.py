from expression import Atom, Summation
class Cursor:
    def __init__(self, x,y):
        self.x = x
        self.y = y

class EditorController:
    def __init__(self):
        self.mode = "normal"
        self.cursor = Cursor(0,0)
        self.lines = [Atom("")]
# ,Summation("i=0", "2", "i + 2")]
        self.vbuffer = ""

    def get_current_line(self):
        return self.lines[self.cursor.y]

    def new_line(self):
        self.lines.insert(self.cursor.y + 1, Atom(""))
        self.cursor.y += 1

    def delete_line(self):
        if self.cursor.y == 0:
            self.lines.pop(0)
            self.lines.insert(0, Atom(""))
            return

        self.lines.pop(self.cursor.y)
        self.cursor.y -= 1


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
        if self.cursor.y == 0:
            return
        self.cursor.y -= 1
    def go_down_line(self):
        if self.cursor.y == len(self.lines) - 1:
            return
        self.cursor.y += 1
