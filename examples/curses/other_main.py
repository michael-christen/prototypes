# See: https://docs.python.org/3/howto/curses.html
import curses
import time

from curses import wrapper


def initialize(fn):
    stdscr = curses.initscr()
    # Turn off automatic echoing of keys
    curses.noecho()
    # Don't require Enter to be pressed
    curses.cbreak()
    # Enable special keys ie) curses.KEY_LEFT
    stdscr.keypad(True)
    try:
        fn(stdscr)
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


def run(stdscr):
    # Clear screen
    stdscr.clear()
    for i in range(0, 9):
        v = i - 10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()


def main():
    wrapper(run)


if __name__ == '__main__':
    main()
