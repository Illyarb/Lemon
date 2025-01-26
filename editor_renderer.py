

def render_editor(editor):
    clear_screen()
    draw_footer(editor)
    move_cursor(0,0)
    for no, line in enumerate(editor.lines):
        # render_line(line,editor, no)
        render(0, no, line)



