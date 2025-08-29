'''
Created on 2025/08/26

@author: sin

.   A floor space
^   A trap (known)
;   A glyph of warding
'   An open door      
<   A staircase up    
>   A staircase down  
#   A wall
+   A closed door
%   A mineral vein
*   A mineral vein with treasure
:   A pile of rubble     
!   A potion (or flask)            
?   A scroll (or book)             
,   A mushroom (or food)           
-   A wand or rod                  
_   A staff                        
=   A ring                         
"   An amulet                      
$   Gold or gems                   
~   Lights, Tools, Chests, etc     
&   Multiple items
/   A pole-arm
|   An edged weapon
\\   A hafted weapon
}   A sling, bow, or x-bow
{   A shot, arrow, or bolt
(   Soft armour
[   Hard armour
]   Misc. armour
)   A shield
'''
import curses
import sys
import time
import logging

class Sokoban:
    SYMBOL_WALL = '#'
    SYMBOL_FLOOR = ' '
    SYMBOL_PLAYER = '@'
    SYMBOL_BOX = '$'
    SYMBOL_GOAL ='.'
    SYMBOL_PLAYER_ON_GOAL = '+'
    SYMBOL_BOX_ON_GOAL = '*'
    
    def __init__(self, level : str):
        self.walls = set()
        self.player_pos = (0,0)
        self.boxes = set()
        self.goals = set()
        self.initial_map = [row for row in level.split('\n') if len(row)]
        self.floor_size = (len(self.initial_map), len(self.initial_map[0]))
        self.set_floor_by_row_strings(self.initial_map)
        self.motion_history = list()

    @property
    def size(self):
        return self.floor_size
    
    @property
    def player(self):
        return self.player_pos
    
    def set_floor_by_row_strings(self, row_strings):
        for row in range(self.floor_size[0]):
            for col in range(self.floor_size[1]):
                sym = row_strings[row][col]
                if sym == self.SYMBOL_WALL :
                    self.walls.add( (row, col) )
                elif sym == self.SYMBOL_PLAYER: 
                    self.player_pos = (row, col)
                elif sym == self.SYMBOL_GOAL :
                    self.goals.add( (row, col) )
                elif sym == self.SYMBOL_BOX :
                    self.boxes.add( (row, col) )
                elif sym == self.SYMBOL_BOX_ON_GOAL :
                    self.boxes.add( (row, col) )
                    self.goals.add( (row, col) )
                elif sym == self.SYMBOL_PLAYER_ON_GOAL :
                    self.player_pos = (row, col)
                    self.goals.add( (row, col) )
                    
        
    def get_row_strings(self):
        map_dict = dict()
        for r,c in self.walls:
            map_dict[(r,c)] = self.SYMBOL_WALL
        for r,c in self.goals:
            map_dict[(r,c)] = self.SYMBOL_GOAL
        for r,c in self.boxes:
            if (r,c) in self.goals :
                map_dict[(r,c)] = self.SYMBOL_BOX_ON_GOAL
            else:
                map_dict[(r,c)] = self.SYMBOL_BOX
        if self.player_pos in self.goals :
            map_dict[self.player_pos] = self.SYMBOL_PLAYER_ON_GOAL
        else:
            map_dict[self.player_pos] = self.SYMBOL_PLAYER 
        #
        rows = list()
        for row in range(self.floor_size[0]):
            rows.append('')
            for col in range(self.floor_size[1]):
                if (row, col) in map_dict :
                    rows[row] = rows[row] + map_dict[(row, col)]
                else:
                    rows[row] = rows[row] + self.SYMBOL_FLOOR
        return rows
    
    def collides(self, row, col):
        pos = (row, col)
        return pos in self.walls or pos in self.boxes 
    
    def move(self, row_dir, col_dir):
        new_pos = (self.player_pos[0] + row_dir, self.player_pos[1] + col_dir)
        if not self.collides(new_pos[0], new_pos[1]) :
            self.motion_history.append( (self.SYMBOL_PLAYER, self.player_pos, new_pos) )
            self.player_pos = new_pos
            return True
        elif new_pos in self.boxes and not self.collides(new_pos[0]+row_dir, new_pos[1]+col_dir) :
            self.motion_history.append( (self.SYMBOL_PLAYER, self.player_pos, new_pos) )
            self.player_pos = new_pos
            self.motion_history.append( (self.SYMBOL_BOX, new_pos, (new_pos[0]+row_dir, new_pos[1]+col_dir)) )
            self.boxes.remove(new_pos)
            self.boxes.add( (new_pos[0]+row_dir, new_pos[1]+col_dir) )
            return True
            
        '''the move is forbidden, floor_map has not been changed'''
        return None
    
    def undo_last_move(self):
        while self.motion_history :
            last_move = self.motion_history.pop()
            if last_move[0] == self.SYMBOL_PLAYER :
                self.player_pos = last_move[1]
                return 
            elif last_move[0] == self.SYMBOL_BOX :
                self.boxes.remove(last_move[2])
                self.boxes.add(last_move[1])
        raise Exception('Motion history rewind Error!')
    
    def check_finished(self):
        for pos in self.boxes:
            if pos not in self.goals :
                return False
        return True


logging.basicConfig(level=logging.INFO, filename='messages.log', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
globals = dict()

def main(stdscr):
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)
    stdscr.clear()
    scr_height, scr_width = stdscr.getmaxyx()
    
    timer_started = time.time()
    
    # keymap = {259: 'up', 258 : 'down', 261: 'right', 260: 'left', 81: 'Q', 113: 'q'}
    # Define game board (simplified example)
    sokoban_map = Sokoban(globals['levels'][globals['floor_no']])
    if sokoban_map.size[0] + 2 > scr_height or sokoban_map.size[1] > scr_width :
        stdscr.addstr(scr_height-1,0,f'Error: size {sokoban_map.size} of the floor exceeds screen size {(scr_height, scr_width)}')
        stdscr.refresh()
        while True : pass
    # logger.info(f'{sokoban_map.size}')
    
    key = 0
    updated = [True for _ in range(sokoban_map.size[0])]
    # logger.info(f'{len(updated)} {updated}')
    stdscr.clear()
    while True:
        # Draw the level
        for y, rowstr in enumerate(sokoban_map.get_row_strings()):
            #logger.info(f'{(y, rowstr)}')
            if updated[y] :
                stdscr.addstr(y, 0, rowstr)
                updated[y] = False
        stdscr.addstr(scr_height-2,0, f'Elapsed {time.time()-timer_started:5.1f}');

        if sokoban_map.check_finished() :
            stdscr.addstr(scr_height-1,0, f'Congratulations!!!');
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.ERR :
            continue
        player_dir = None
        if key == ord('q'):
            break  # Quit
        elif key == curses.KEY_UP:
            player_dir = [-1, 0]
        elif key == curses.KEY_LEFT:
            player_dir = [0, -1]
        elif key == curses.KEY_RIGHT:
            player_dir = [0, +1]
        elif key == curses.KEY_DOWN:
            player_dir = [+1, 0]
        # if the player bumps
        if player_dir :
            if sokoban_map.move(player_dir[0], player_dir[1]) :
                pos = sokoban_map.player
                rmin = max(pos[0] - 1, 0)
                rmax = min(pos[0] + 1, sokoban_map.size[0]+1 )
                for r in range(rmin, rmax + 1) :
                    updated[r] = True
            else:
                curses.beep()
        elif key == ord('r') :
            curses.beep()
            sokoban_map.undo_last_move()
            for r in range(sokoban_map.size[0]) :
                updated[r] = True

# Run the curses application
if __name__ == '__main__':
    # read flooor maps (levels)
    levels = list()
    with open('floors.txt', 'r') as f :
        for a_line in f:
            a_line = a_line.strip()
            if len(levels) == 0 :
                levels.append('')
            if len(a_line) == 0 and len(levels[-1]) > 0 :
                levels.append('')
            else:
                levels[-1] = levels[-1] + a_line + '\n'
    #logger.info(f'levels[-1] = {levels[-1]}')
    #logger.info(f'{levels[1]}')
    #logger.info(f'len ={len(levels)}')
    globals['levels'] = levels
    try:
        globals['floor_no'] = int(sys.argv[1])
    except:
        globals['floor_no'] = 1
    #
    curses.wrapper(main)
    
        