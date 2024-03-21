from AppKit import NSScreen


def get_screen_resolution():
    screen = NSScreen.mainScreen()
    screen_dimensions = screen.frame().size
    width, height = screen_dimensions.width, screen_dimensions.height
    return width, height
