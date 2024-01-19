import curses


attributes = [
    curses.A_BLINK,
    curses.A_BOLD,
    curses.A_DIM,
    curses.A_REVERSE,
    curses.A_STANDOUT,
    curses.A_UNDERLINE,
]


def main(stdscr):
    # Clear
    stdscr.clear()
    # Setup colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)

    # Make it highly visible
    curses.curs_set(2)

    statements = {
        'joe': 'Heyo',
        'karl': 'zamboni is on the ice',
        'bob': 'build',
    }
    names = sorted(statements.keys())
    y, x = (0, 0)
    stmt = ''

    while True:
        y = min(max(y, 0), curses.LINES - 1)
        x = min(max(x, 0), curses.COLS - 1)
        # Highlight line we're on
        for i, name in enumerate(names):
            if i == y:
                attr = curses.A_UNDERLINE
            else:
                attr = 0
            stdscr.addstr(i, 0, name, attr)
        # Say something on status line if we want to
        stdscr.addstr(curses.LINES-1, 0, stmt, curses.A_STANDOUT)
        # Clear whole line
        stdscr.clrtoeol()

        stdscr.move(y, x)
        stdscr.refresh()

        y, x = stdscr.getyx()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            y -= 1
        elif key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_LEFT:
            x -= 1
        elif key == curses.KEY_RIGHT:
            x += 1

        if key == curses.KEY_ENTER or key == 10:
            stmt_selection = y
        else:
            stmt_selection = None

        if stmt_selection is not None and stmt_selection < len(names):
            stmt = statements[names[stmt_selection]]
        else:
            stmt = ''

def misc():
    curses.beep()


if __name__ == '__main__':
    curses.wrapper(main)
