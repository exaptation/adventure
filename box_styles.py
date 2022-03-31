# These are the special characters used to draw the
# boxes.


def get_styles():
    styles = {
        "heavy": {
            "top_left": "┏",
            "top_right": "┓",
            "horizontal": "━",
            "vertical": "┃",
            "bottom_left": "┗",
            "bottom_right": "┛",
        },
        "light": {
            "top_left": "┌",
            "top_right": "┐",
            "horizontal": "─",
            "vertical": "│",
            "bottom_left": "└",
            "bottom_right": "┘",
        },
        "dotted": {
            "top_left": "┌",
            "top_right": "┐",
            "horizontal": "┈",
            "vertical": "┊",
            "bottom_left": "└",
            "bottom_right": "┘",
        },
        "double": {
            "top_left": "╔",
            "top_right": "╗",
            "horizontal": "═",
            "vertical": "║",
            "bottom_left": "╚",
            "bottom_right": "╝",
        },
    }
    return styles
