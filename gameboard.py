import box_styles
import color_schemes
import rooms

# This stores the game configuration information
# necessary to draw the UI.


def build_game(start_line=1, start_column=2, game_width=55):
    game = {
        "settings": build_settings(start_line, start_column, game_width),
        "styles": box_styles.get_styles(),
        "color_schemes": color_schemes.build_color_scheme(),
        "transitions": build_transitions(),
        "player": build_player(),
        "menus": build_menus(),
        "rooms": rooms.build_rooms(),
        "items": rooms.build_items(),
        "details": rooms.build_details(),
    }
    game.update({"boxes": build_boxes(game)})
    game.update({"ui_text": build_ui_text(game)})
    return game


def build_settings(start_line, start_column, game_width):
    settings = {
        "start_line": start_line,
        "start_column": start_column,
        "game_width": game_width,
        "top_padding": 1,
        "right_padding": 4,
        "bottom_padding": 1,
        "left_padding": 4,
        "text_padding": 2,
        "text_speed": 30,
        "text_color": 15,
        "max_name": 9,
        "min_name": 3,
        "transition_speed": 100,
        "pulse_speed": 10,
        "ui_delay": 1.5,
    }
    return settings


def build_ui_text(game):
    settings = game.get("settings")
    max_name = settings.get("max_name")
    min_name = settings.get("min_name")
    ui_text = {
        "loading1": ["Loading Game...", "Detecting terminal size..."],
        "loading2": [
            "Terminal test passed...",
            "Channeling mana from the rift...",
            "Polishing adamatine armor...",
            "Here we go...",
        ],
        "title": "* a c c e n t u r e   a d v e n t u r e *".upper(),
        "too_long": "name too long".capitalize(),
        "too_short": "name too short".capitalize(),
        "name_prompt": (
            "Greetings brave ACCENTURER! "
            "Many great adventures await you. "
            "Tell us your name such that the bards can sing "
            "your tales for eons to come!"
        ),
        "enter_name": "Enter your name",
        "scribe": "'s name inscribed in Book of Deeds!",
        "max_name": (f"Please enter a name under {max_name} charecters."),
        "min_name": (f"Please enter a name over {min_name} characters."),
    }
    return ui_text


def build_player():
    player = {
        "box": "Unknown",
        "job": "Peasant",
        "door": "Default",
        "current_room": "main",
        "start_room": "main",
        "item_list": ["apple"],
        "max_items": 8,
        "turn_count": 0,
        "navigation": ["user"],
    }
    return player


def build_boxes(game):
    settings = game.get("settings")
    start_line = settings.get("start_line")
    start_column = settings.get("start_column")
    border_width = settings.get("game_width")
    top_pad = settings.get("top_padding")
    right_pad = settings.get("right_padding")
    bottom_pad = settings.get("bottom_padding")
    left_pad = settings.get("left_padding")
    text_padding = settings.get("text_padding")
    inner_column = start_column + right_pad
    inner_width = border_width - right_pad - left_pad
    line_height = 1

    # inner boxes
    inner = {
        "title": {"height": 3, "style": "double"},
        "info": {"height": 3, "style": "heavy"},
        "dialogue": {"height": 13, "style": "double"},
        "response": {"height": 3, "style": "heavy"},
        "options": {"height": 6, "style": "double"},
        "input": {"height": 3, "style": "heavy"},
    }
    # outer boxes
    outer = {"border": {}}

    # Calculates the height of all inner boxes
    inner_height = 0
    for item in inner:
        inner_height += inner[item].get("height")

    border_height = 2 + inner_height + top_pad + bottom_pad

    accumulate = start_line + line_height + top_pad
    for box in inner:
        inner.get(box).update({"line": accumulate})
        inner.get(box).update({"width": inner_width})
        inner.get(box).update({"column": inner_column})
        inner.get(box).update({"start": accumulate + line_height})
        end = inner.get(box).get("start") + inner.get(box).get("height") - 3
        inner.get(box).update({"end": end})
        text_height = inner.get(box).get("height") - 2
        inner.get(box).update({"text_height": text_height})
        text_start = inner.get(box).get("column") + text_padding
        inner.get(box).update({"text_start": text_start})
        text_width = inner.get(box).get("width") - text_padding * 2
        inner.get(box).update({"text_width": text_width})
        accumulate += inner.get(box).get("height")

    # border box
    outer.get("border").update({"height": border_height})
    outer.get("border").update({"style": "double"})
    outer.get("border").update({"line": start_line})
    outer.get("border").update({"width": border_width})
    outer.get("border").update({"column": start_column})
    outer.get("border").update({"start": start_line + line_height})
    outer.get("border").update({"end": border_height - line_height})

    # all boxes
    boxes = {"inner": inner, "outer": outer}

    return boxes


def build_transitions():
    transitions = {
        "purple_grade": [91, 92, 93],
        "blue_grade": [19, 20, 21],
        # dark_to_light = range(236, 255)
        "fade_in": [236, 255],
    }
    return transitions


def build_menus():
    menus = {
        "user": {
            "options": [
                "look",
                "inspect",
                "interact",
                "get",
                "move",
                "inventory",
                "settings",
                "quit",
            ],
            "prompt": "Choose Option",
        },
        "inspect": {
            "prompt": "Select Detail",
            "nothing": "Nothing to inspect",
            "options": ["back"],
        },
        "interact": {
            "prompt": "Select Interaction",
            "nothing": "Nothing to interact",
            "options": ["back"],
        },
        "inventory": {
            "options": [
                "examine",
                "use",
                "drop",
                "back",
            ],
            "prompt": "Inventory",
            "nothing": "Inventory Empty",
        },
        "get": {
            "prompt": "Select Item",
            "nothing": "Nothing to get",
            "options": ["back"],
        },
        "move": {
            "prompt": "Select Location",
            "nothing": "Nowhere to go",
            "options": ["back"],
            "success": "You adventure to the ",
        },
        "drop": {
            "prompt": "Select Item",
            "nothing": "Nothing to drop",
            "options": ["back"],
        },
        "settings": {
            "prompt": "Select Setting",
            "options": ["back"],
        },
        "quit": {
            "prompt": "Would you like to quit?",
            "options": ["yes", "no"],
        },
        "examine": {
            "prompt": "Select Item",
            "nothing": "Nothing to examine",
            "options": ["back"],
        },
        "use": {
            "prompt": "Selection Item",
            "nothing": "Nothing to use",
            "options": ["back"],
        },
    }
    return menus
