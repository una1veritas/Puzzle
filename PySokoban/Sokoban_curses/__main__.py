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
from collections import deque
import pygame

class Sokoban:
    SYMBOL_WALL = '#'
    SYMBOL_FLOOR = ' '
    SYMBOL_WOOD_FLOORING = '-'
    SYMBOL_PLAYER = '@'
    SYMBOL_BOX = '$'
    SYMBOL_GOAL ='.'
    SYMBOL_PLAYER_ON_GOAL = '+'
    SYMBOL_BOX_ON_GOAL = '*'
    
    def __init__(self, level : str):
        logger.info(f'level = {level}')
        self.walls = set()
        self.player_pos = (0,0)
        self.boxes = set()
        self.goals = set()
        self.initial_map = [row for row in level.strip().split('\n') if len(row)]
        max_width = max([len(row) for row in self.initial_map])
        self.floor_size = (len(self.initial_map), max_width)
        logger.info(f'{self.floor_size}')
        self.set_floor_by_row_strings(self.initial_map)
        self.motion_history = list()

    def restart(self):
        self.walls.clear()
        self.player_pos = (0,0)
        self.boxes.clear()
        self.goals.clear()
        self.set_floor_by_row_strings(self.initial_map)

    @property
    def size(self):
        return self.floor_size
    
    @property
    def player(self):
        return self.player_pos
    
    def set_floor_by_row_strings(self, row_strings):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if not col < len(row_strings[row]) :
                    continue
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
                elif sym == self.SYMBOL_FLOOR or sym == self.SYMBOL_WOOD_FLOORING :
                    pass 
                    
        
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
        for row in range(self.size[0]):
            rows.append('')
            for col in range(self.size[1]):
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
        while len(self.motion_history) > 0 :
            last_move = self.motion_history.pop()
            if last_move[0] == self.SYMBOL_PLAYER :
                self.player_pos = last_move[1]
                return True
            elif last_move[0] == self.SYMBOL_BOX :
                self.boxes.remove(last_move[2])
                self.boxes.add(last_move[1])
        #raise Exception('Motion history rewind Error!')
        return False
    
    def check_finished(self):
        for pos in self.boxes:
            if pos not in self.goals :
                return False
        return True


logging.basicConfig(level=logging.INFO, filename='messages.log', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
globals = dict()
#pygame.mixer.init()
#pygame.mixer.music.load('walk-steps.wav')
# play_obj = wave_obj.play()
# play_obj.wait_done() # Waits until sound has finished playing
    
def main(stdscr):
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)
    stdscr.clear()
    scr_height, scr_width = stdscr.getmaxyx()
    
    while True:
        timer_started = time.time()
        
        # keymap = {259: 'up', 258 : 'down', 261: 'right', 260: 'left', 81: 'Q', 113: 'q'}
        # Define game board (simplified example)
        selected_level = globals['levels'][globals['floor_no']]
        sokoban_map = Sokoban(selected_level[0])
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
            stdscr.addstr(scr_height-3,0, f'size size {sokoban_map.size}');
    
            if sokoban_map.check_finished() :
                stdscr.addstr(scr_height-1,0, f'Congratulations!!!');
                break       
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == curses.ERR :
                continue
            player_dir = None
            if key == ord('q'):
                return  # Quit
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
                    #pygame.mixer.music.play() 
                    pos = sokoban_map.player
                    rmin = max(pos[0] - 1, 0)
                    rmax = min(pos[0] + 1, sokoban_map.size[0]+1 )
                    for r in range(rmin, rmax + 1) :
                        updated[r] = True
                else:
                    curses.beep()
            elif key == ord('u') :
                curses.beep()
                sokoban_map.undo_last_move()
                for r in range(sokoban_map.size[0]) :
                    updated[r] = True
            elif key == ord('r') :
                curses.beep()
                sokoban_map.restart()
                for r in range(sokoban_map.size[0]) :
                    updated[r] = True
        globals['floor_no'] += 1

def load_levels(filename):
    levels = list()
    buffer = deque()
    with open(filename, 'r') as file :
        while (a_line := file.readline() ) != '' :
            a_line = a_line.strip()
            buffer.append(a_line)
            items = a_line.split(':')
            level_info = dict()
            if items[0] == 'Title' :
                buffer.pop()
                level_info['Title'] = items[1].strip()
                while (a_line := file.readline() ) != '' :
                    if len(a_line.strip()) == 0 :
                        break
                    if ':' in a_line :
                        items = a_line.split(':')
                        level_info[items[0]] = ':'.join(items[1:])
                    else:
                        level_info[items[0]] += a_line.strip()
                level_info['floor'] = list()
                for l in reversed(buffer):
                    if len(l) == 0 :
                        break
                    level_info['floor'].append(l)
                if len(level_info['floor']) == 0 :
                    print(level_info)
                    raise Exception('format error!!')
                level_info['floor'].reverse()
                level_info['floor'] = '\n'.join(level_info['floor'])
                buffer.clear()
                levels.append( list() )
                levels[-1].append( level_info['floor'] )
                if 'Title' in level_info :
                    levels[-1].append( level_info['Title'] )
                if 'Comment' in level_info :
                    levels[-1].append( level_info['Comment'] )
    return levels

# Run the curses application
if __name__ == '__main__':
    # read flooor maps (levels)
    if len(sys.argv) > 1 :
        file_name = sys.argv[1]
    else:
        file_name = 'floor.txt'
    levels = load_levels(file_name)
    
    #logger.info(f'levels[-1] = {levels[-1]}')
    #logger.info(f'{levels[1]}')
    logger.info(f'{levels}')
    globals['levels'] = levels
    try:
        globals['floor_no'] = int(sys.argv[2])
    except:
        globals['floor_no'] = 0
    #
    curses.wrapper(main)
    
        