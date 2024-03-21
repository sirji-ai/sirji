from sirji.view.terminal import open_terminal_and_run_command
from sirji.view.screen import get_screen_resolution


def main():
    screen_width, screen_height = get_screen_resolution()
    margin = 5  # Margin size in pixels
    window_width = (screen_width - 3 * margin) // 2
    window_height = (screen_height - 22 - 4 * margin) // 3

    command_title_pairs = [
        ("echo Welcome to Sirji;tail -f log/sirji.log", "Sirji Chat"),
        ("tail -f logs/sirji.log", "Sirji Logs"),
        ("tail -f logs/planner.log", "Planner Logs"),
        ("tail -f logs/researcher.log", "Researcher Logs"),
        ("tail -f logs/coder.log", "Coder Logs"),
        ("tail -f logs/executor.log", "Executor Logs")
    ]

    for i, (command, title) in enumerate(command_title_pairs):
        open_terminal_and_run_command(
            command, title, i, window_width, window_height)

    print("Terminals opened and arranged in a 3x2 grid with 5px margins.")


if __name__ == "__main__":
    main()
