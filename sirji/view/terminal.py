import subprocess

def run_applescript(script):
    subprocess.run(["osascript", "-e", script], text=True)


def open_terminal_and_run_command(command, title, position_index, w, h):
    margin = 5  # Margin size in pixels
    positions = [
        (margin, 22 + margin),  # First row, first column
        (w + 2 * margin, 22 + margin),  # First row, second column
        (margin, h + 2 * margin + 22),  # Second row, first column
        (w + 2 * margin, h + 2 * margin + 22),  # Second row, second column
        (margin, 2 * h + 3 * margin + 22),  # Third row, first column
        (w + 2 * margin, 2 * h + 3 * margin + 22),  # Third row, second column,
    ]
    x, y = positions[position_index % 6]
    adjusted_width = w - margin
    adjusted_height = h - margin

    apple_script_command = f'''
        tell application "Terminal"
            activate
            do script "{command}"
            delay 1
            set the bounds of the front window to {{{x}, {y}, {x + adjusted_width}, {y + adjusted_height}}}
            set custom title of tab 1 of front window to "{title}"
        end tell
        delay 1
        '''
    run_applescript(apple_script_command)
