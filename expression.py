from tui import *

class Expression: 
    def __init__(self,value=None, width=0, height=0):
        self.value = value
        self.width = width
        self.height = height

    def __len__(self): 
        return self.width

    def __str__(self):
        return str(self.value)

    def set_value(self, value):
        self.value = value

    def focus(self):
        self.isFocused = True

    def unfocus(self):
        self.isFocused = False

class Atom(Expression):
    def __init__(self,value,  x = 0 , y =0, cursor_x=0, cursor_y=0,start_at_zero = True):
        self.x = x
        self.y = y
        self.value = value
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.width = len(value)
        self.start_at_zero = start_at_zero
        self.height = 1
        self.isFocused = False

    def replace(self, fr, to):
        return self.value.replace(fr, to)
   
    def get_char_at_cursor(self):
        if self.cursor_x == 0 or self.width == 0:
            return "□"
        else:
            try:
                return self.value[self.cursor_x-1]
            except:
                return "□"

    def get_cursor_string(self):
        if(self.cursor_x == self.width):
            l = self.value
            r = "" 
        elif(self.cursor_x == 0):
            l = ""
            r = self.value
        else:
            l = self.value[:self.cursor_x]
            r = self.value[self.cursor_x:]
        return l  + "│"  + r

    def get_string(self):
        return self.value

    def __len__(self):
        return len(self.value)

    def get_cursors(self):
        return str("Atom: ("+str(self.cursor_x)+")")

    def get_widths(self):
        return str("Atom: ("+str(self.width)+")")


    def type_char(self, char):
        self.cursor_x += 1
        self.value = self.value[:self.cursor_x] + char + self.value[self.cursor_x:]
        self.width += 1
        return self

    def go_left(self):
        if self.cursor_x == 0:
            return False 
        elif self.cursor_x == 1 and self.start_at_zero == False:
            return False
        else:
            self.cursor_x -= 1
            return True

    def go_right(self):
        if self.cursor_x < self.width:
            self.cursor_x += 1
            return True
        else:
            return False

    def backspace(self):
        if self.cursor_x >= 0 and len(self.value) > 0:
            self.value = self.value[:self.cursor_x-1] + self.value[self.cursor_x:]
            self.width -= 1
            if self.start_at_zero == False and self.cursor_x == 1: 
                self.cursor_x = 1
            else:
                self.cursor_x -= 1
        if self.start_at_zero == True and self.cursor_x == 0:
            self.cursor_x = 1
        return self
    
    def render(self):
        if self.isFocused:
            putstr(self.get_cursor_string())
        else:
            putstr(self.value)
        

class Matrix(Expression):
    def __init__(self, rows, cols, values, cursor_x=0, cursor_y=0):
        self.rows = rows
        self.cols = cols
        self.values = values
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.height = len(values)
        _width = 0 
        for row in values:
            for val in row:
                _width += len(val)
        self.width = _width + len(self.values[0])

    def go_left(self):
        if self.cursor_x == 0:
            return False
        else:
            self.cursor_x -= 1
            return True

    def go_right(self):
        if self.cursor_x < self.cols:
            self.cursor_x += 1
            return True
        else:
            return False
    def go_up(self):
        if self.cursor_y == 0:
            return False
        else:
            self.cursor_y -= 1
            return True
    def go_down(self):
        if self.cursor_y < self.rows:
            self.cursor_y += 1
            return True
        else:
            return False

    def backspace(self):
        self.values[self.cursor_y][self.cursor_x] = self.values[self.cursor_y][self.cursor_x][:-1]

    def type_char(self, char):
        self.values[self.cursor_y][self.cursor_x] += char

    def get_string(self):
        return ""

    def get_cursor_string(self):
        return ""
    def get_cursors(self):
        return ""
    def get_widths(self):
        return ""

    def get_row_width(self, n):
        _width = 0
        row = self.values[n]
        for val in row:
            _width += len(val)
        return _width
    
    def get_highest_row_width(self):
        _width = 0
        for row in self.values:
            for val in row:
                _width += len(val)
        return _width

    def render(self):
        putstr("┌" + " " * (self.get_highest_row_width() + self.width) + "┐") 
        move_cursor_down(1)
        for row in self.values:
            putstr("│ ")
            for val in row:
                putstr(val + " ") 
            putstr("│")
            move_cursor_down(1)
            move_cursor_left(self.get_highest_row_width())
        move_cursor_down(2)
        putstr("└" + " " * (self.width-1) + "┘")





class Summation(Expression):
    def __init__(self, lower, upper,summand,height=3,width=2):
        self.lower = lower
        self.upper = upper
        self.summand = summand
        self.cursor_state = "summand"
        self.height = height
        self.width = width
        self.isFocused = False

    def render(self):
        clear_images()
        move_cursor_right(1)
        putstr(self.upper)
        move_cursor_left(1)
        display_image(sum_image, 2,2)
        move_cursor_down(2)
        move_cursor_right(4)
        putstr(self.summand)
        move_cursor_down(1)
        move_cursor_left(3)
        putstr(self.lower)

    def go_left(self):
        pass
    def go_right(self):
        pass
    def gou_up(self):
        pass
    def go_down(self):
        pass
    def backspace(self):
        pass
    def type_char(self, char):
        pass
    def get_string(self):
        return ""
    def get_cursor_string(self):
        return ""
    def get_cursors(self):
        return ""
    def get_widths(self):
        return ""

