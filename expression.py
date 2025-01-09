class Expression: 
    def __init__(self,value=None):
        self.value = value

    def __len__(self): 
        return self.width

    def __str__(self):
        return str(self.value)


    def set_value(self, value):
        self.value = value

class Atom(Expression):
    def __init__(self, value, cursor_x=0, cursor_y=0,start_at_zero = True):
        self.value = value
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.width = len(value)
        self.start_at_zero = start_at_zero
        self.height = 1

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

class Sum(Expression):
    def __init__(self, lower, upper,summand):
        self.lower = lower
        self.upper = upper
        self.summand = summand
        self.cursor_state = "summand"





