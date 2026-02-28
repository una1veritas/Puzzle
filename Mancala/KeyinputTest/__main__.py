'''
Created on 2026/02/26

@author: sin
'''

import time
from pynput import keyboard

# 1. Define a custom exception
class KeyPressedException(Exception):
    """Custom exception to be raised when a specific key is pressed."""
    pass

def on_press(key):
    """Callback function for the keyboard listener."""
    # Check if the pressed key is the 'esc' key
    if key == keyboard.Key.esc:
        # 3. Raise the custom exception
        raise KeyPressedException(key)
    try:
        # You can also check for a specific character key, e.g., 'q'
        if key.char == 'q':
            raise KeyPressedException(key.char)
    except AttributeError:
        # Handle cases where key doesn't have a .char attribute (like special keys)
        pass

# Main program execution
if __name__ == '__main__':
    print("Program started. Press 'Esc' or 'q' to raise an exception and stop the loop.")
    
    # 2. Set up the listener in a 'with' statement for proper resource management
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            # 4. Handle the exception
            while True:
                # Your main program logic goes here
                print("Doing work... (Ctrl+C will also work due to KeyboardInterrupt inheritance)")
                time.sleep(1)
        except KeyPressedException as e:
            print(f"Caught the custom exception: {e.args[0]} was pressed.")
            listener.stop() # Stop the listener gracefully
        except KeyboardInterrupt:
            # You can also handle the standard Ctrl+C interrupt
            print("Program interrupted by Ctrl+C.")
            listener.stop()
        finally:
            print("Program finished.")
            # Ensure the listener thread is joined
            listener.join()

    pass