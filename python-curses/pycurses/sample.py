'''
Created on 2019/09/22

@author: Sin Shimozono
'''
import curses


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.refresh()
    posx = 0
    posy = 1
    prevx = posx
    prevy = posy
    while True:
        ch = stdscr.getch()            # scan a pressed key 
        if ch != -1 :
            prevx = posx
            prevy = posy
            if ch == ord('Q') or ch == ord('q') :
                break
            elif ch == curses.KEY_UP :
                posy = max(1, posy-1)
            elif ch == curses.KEY_DOWN :
                posy = min(24, posy+1)
            elif ch == curses.KEY_LEFT :
                posx = max(0, posx-1)
            elif ch == curses.KEY_RIGHT :
                posx = min(80, posx+1)
            stdscr.addstr(0,0,str(posx)+' '+str(posy))
            stdscr.addstr(prevy, prevx, '   ')
            stdscr.addstr(posy, posx, str(ch))
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
