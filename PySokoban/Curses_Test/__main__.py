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
import time

class Sokoban_map:
    SYMBOL_WALL = '#'
    SYMBOL_FLOOR = ' '
    SYMBOL_PLAYER = '@'
    SYMBOL_BOX = '$'
    SYMBOL_DESTINATION ='.'
    
    def __init__(self, level : str):
        self.walls = set()
        self.player = (0,0)
        self.boxes = set()
        self.goals = set()
        self.initial_map = [row for row in level.split('\n') if len(row)]
        self.size = (len(self.initial_map), len(self.initial_map[0]))
        self.set_by_row_strings(self.initial_map)
        self.motion_history = list()
    
    def set_by_row_strings(self, row_strings):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                sym = row_strings[row][col]
                if sym == self.SYMBOL_WALL :
                    self.walls.add( (row, col) )
                elif sym == self.SYMBOL_PLAYER: 
                    self.player = (row, col)
                elif sym == self.SYMBOL_DESTINATION :
                    self.goals.add( (row, col) )
                elif sym == self.SYMBOL_BOX :
                    self.boxes.add( (row, col) )
        
    def get_row_strings(self):
        map_dict = dict()
        for r,c in self.walls:
            map_dict[(r,c)] = self.SYMBOL_WALL
        for r,c in self.boxes:
            map_dict[(r,c)] = self.SYMBOL_BOX
        map_dict[(self.player[0], self.player[1])] = self.SYMBOL_PLAYER
        rows = list()
        for row in range(self.size[0]):
            rows.append('')
            for col in range(self.size[1]):
                if (row, col) in map_dict :
                    rows[row] = rows[row] + map_dict[(row, col)]
                else:
                    if (row, col) in self.goals:
                        rows[row] = rows[row] + self.SYMBOL_DESTINATION
                    else:
                        rows[row] = rows[row] + self.SYMBOL_FLOOR
        return rows
    
    def player_pos(self):
        return self.player
    
    def collides(self, row, col):
        pos = (row, col)
        return pos in self.walls or pos in self.boxes 
    
    def move(self, row_dir, col_dir):
        new_pos = (self.player[0] + row_dir, self.player[1] + col_dir)
        if not self.collides(new_pos[0], new_pos[1]) :
            self.motion_history.append( (self.SYMBOL_PLAYER, self.player, new_pos) )
            self.player = new_pos
            return True
        elif new_pos in self.boxes and not self.collides(new_pos[0]+row_dir, new_pos[1]+col_dir) :
            self.motion_history.append( (self.SYMBOL_PLAYER, self.player, new_pos) )
            self.player = new_pos
            self.motion_history.append( (self.SYMBOL_BOX, new_pos, (new_pos[0]+row_dir, new_pos[1]+col_dir)) )
            self.boxes.remove(new_pos)
            self.boxes.add( (new_pos[0]+row_dir, new_pos[1]+col_dir) )
            return True
            
        '''the move is forbidden, floor_map has not been changed'''
        return False
    
    def rewind_last_move(self):
        while self.motion_history :
            last_move = self.motion_history.pop()
            if last_move[0] == self.SYMBOL_PLAYER :
                self.player = last_move[1]
                return
            elif last_move[0] == self.SYMBOL_BOX :
                self.boxes.remove(last_move[2])
                self.boxes.add(last_move[1])
            else:
                raise Exception('Motion history rewind Error!')
                return
    
    def check_finished(self):
        for pos in self.boxes:
            if pos not in self.goals :
                return False
        return True

    @staticmethod
    def example():
        return [\
        "#########\n" \
        "#   @   #\n" \
        "#       #\n" \
        "#  ##.  #\n" \
        "#   #   #\n" \
        "#  $##. #\n" \
        "#  $    #\n" \
        "#       #\n" \
        "#########", 
        
        "#################\n" \
        "#####   #########\n" \
        "#####$  #########\n" \
        "#####  $#########\n" \
        "###  $  $ #######\n" \
        "### # ### #######\n" \
        "#   # ### ##  ..#\n" \
        "# $  $      @ ..#\n" \
        "##### #### #  ..#\n" \
        "#####      ######\n" \
        "#################\n" 
        ]

def main(stdscr):
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    
    timer_started = time.time()
    
    # keymap = {259: 'up', 258 : 'down', 261: 'right', 260: 'left', 81: 'Q', 113: 'q'}
    # Define game board (simplified example)
    sokoban_map = Sokoban_map(Sokoban_map.example()[1])
    
    key = 0
    while True:
        stdscr.nodelay(True)
        stdscr.clear()
        # Draw the level
        for y, rowstr in enumerate(sokoban_map.get_row_strings()):
            stdscr.addstr(y, 0, rowstr)
        stdscr.addstr(sokoban_map.size[0]+1,0, f'Elapsed {time.time()-timer_started:5.1f}');

        if sokoban_map.check_finished() :
            stdscr.addstr(12,0, f'Congratulations!!!');
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
        elif key == ord('r') :
            curses.beep()
            sokoban_map.rewind_last_move()
            continue
        # check whether the player can move or not
        if player_dir and not sokoban_map.move(player_dir[0], player_dir[1]) :
            curses.beep()

# Run the curses application
if __name__ == '__main__':
    curses.wrapper(main)
    