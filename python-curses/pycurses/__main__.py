'''
Created on 2019/09/22

@author: Sin Shimozono
'''
import curses
from curses import ascii

def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.refresh()
    curses.curs_set(0)
    posx = 0
    posy = 1
    prevx = posx
    prevy = posy
    character = '@'
    while True:
        ch = stdscr.getch()            # scan a pressed key 
        if ch != -1 :
            prevx = posx
            prevy = posy
            if ch == curses.KEY_UP :
                posy = max(1, posy-1)
            elif ch == curses.KEY_DOWN :
                posy = min(23, posy+1)
            elif ch == curses.KEY_LEFT :
                posx = max(0, posx-1)
            elif ch == curses.KEY_RIGHT :
                posx = min(79, posx+1)
            elif ch == ord('Q') or ch == ord('q') :
                break
            
            stdscr.addstr(0,0,"posx = {0}, posy = {1}".format(posx, posy))
            stdscr.addstr(prevy, prevx, ' ')
            if curses.ascii.isprint(chr(ch)) :
                character = chr(ch)
            stdscr.addstr(posy, posx, character)
            stdscr.refresh()

if __name__ == '__main__' :
# wrapper execute the following mode changes, 
# and after the execution automatically restore 
# the modes of the screen: 
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)
    curses.wrapper(main)
