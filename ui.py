import time
import os
import random


def clear_screen():
    os.system("clear")


# Cursor and location functions
# This console UI is built on escape codes


def show_cursor():
    # This code shows the cursor
    print("\x1b[?25h", end="", flush=True)


def hide_cursor():
    # This code hides the cursor
    print("\x1b[?25l", end="", flush=True)


def set_position(line, column):
    # This code sets the position of the cursor
    # in the terminal.
    print(f"\u001b[{line};{column}f", end="", flush=True)


def set_underline():
    print("\u001b[4m,", end="", flush=True)


def set_bold():
    print("\u001b[1m", end="", flush=True)


def set_cursor(game, box_name="input"):
    # Sets the cursor at the upper left corner
    # of the element.
    inner = get_inner(game)
    border = get_border(game)
    if box_name == "exit":
        line = border.get("line")
        height = border.get("height")
        set_position(line + height + 1, 1)
    else:
        line = inner[box_name].get("start")
        column = inner[box_name].get("text_start")
        set_position(line, column)


# graphic functions


def get_style(game, style_name):
    # Returns a dictionary with the characters
    # of a specific style (heavy, thin, dotted, etc..)
    return game.get("styles").get(style_name)


def draw_box(game, box_obj):
    # Draws the boxes using characters.
    height = box_obj.get("height")
    width = box_obj.get("width")
    line = box_obj.get("line")
    column = box_obj.get("column")
    style_dict = get_style(game, box_obj.get("style"))

    # set style
    top_left = style_dict.get("top_left")
    top_right = style_dict.get("top_right")
    horizontal = style_dict.get("horizontal")
    vertical = style_dict.get("vertical")
    bottom_left = style_dict.get("bottom_left")
    bottom_right = style_dict.get("bottom_right")

    # build lines
    top = f"{top_left}" f"{horizontal * (width - 2)}" f"{top_right}"
    bottom = f"{bottom_left}" f"{horizontal * (width - 2)}" f"{bottom_right}"

    # print top
    set_position(line, column)
    print(top, end="", flush=True)

    # print sides
    set_position(line + 1, column)
    for n in range(1, height - 1):
        set_position(line + n, column)
        print(vertical, end="", flush=True)
        set_position(line + n, column + width - 1)
        print(vertical, end="", flush=True)

    # print bottom
    set_position(line + height - 1, column)
    print(bottom, end="", flush=True)


def draw_box_all(game):
    # Draw border then loop through inner
    draw_box(game, get_border(game))
    inner = get_inner(game)
    for box in inner:
        draw_box(game, inner[box])


def draw_inner(game, inner_name):
    # Draws a single inner box
    inner = get_inner(game)
    draw_box(game, inner[inner_name])


def draw_border(game):
    # Draws the border
    border = get_border(game)
    draw_box(game, border)


# special effects and transitions


def transition_all(game, trans):
    hide_cursor()
    transition = game.get("transitions").get(trans)
    speed = get_setting(game, "transition_speed") / 1000
    for color_code in transition:
        draw_box_all(game, color_code)
        time.sleep(speed)


def pulse_all(game, transition, count):
    speed = get_setting(game, "pulse_speed")
    pulses = range(count)
    for pulse in pulses:
        time.sleep(speed / 1000)
        transition_all(game, transition)


def eat_strange_berries(game, char="*"):
    hide_cursor()
    for x in range(30):
        for n in range(1):
            set_random_color(game)
            draw_box_all(game)
        for y in range(5):
            rainbow_fill_all(game, char)
    turns = random.randint(1, 4)
    increment_turn(game, turns)
    set_player(game, "current_room", "forest")
    add_room_item(game, "strange berries")
    show_cursor()


# Functions for managing terminal colors
# Color related functions


def get_color(color_code):
    # Returns color code or reset code with -1
    reset = "\u001b[0m"
    if color_code == -1:
        return f"{reset}"
    else:
        return f"\u001b[38;5;{color_code}m"


def set_color(color_code):
    color_code = get_color(color_code)
    print(color_code, end="", flush=True)


def set_random_color(game):
    # Sets a random color outside of the greyscale range
    color_code = random.randint(1, 231)
    set_color(color_code)


def get_random_color(game):
    # Returns the code for a random color outside of the
    # greyscale range
    color_code = random.randint(1, 231)
    return color_code


# text and input functions


def pause_game(game):
    # Pauses game until enter is pressed.
    print_response(game, "Press ENTER to continue")
    collect_input(game)
    fill_box(game, "response")


def print_dialogue_lines(game, message_list):
    # Takes a list of lines.
    # Slow prints the dialogue to simulate speech.
    # When the text fills the box simulates scrolling
    # by printing text height -1 lines then resumes
    # slow printing.
    set_room_text_color(game, "dialogue")
    fill_box(game, "dialogue")
    dialogue = get_inner(game).get("dialogue")
    line = dialogue.get("start")
    column = dialogue.get("text_start")
    threshold = dialogue.get("text_height") - 1
    pause_counter = 0

    for n in range(len(message_list)):
        if n < threshold:
            set_position(line, column)
            speak_print(game, message_list[n])
            line += 1
        else:
            line2 = dialogue.get("start")
            fill_box(game, "dialogue")
            for message in message_list[n - threshold: n]:
                set_position(line2, column)
                print(message)
                line2 += 1
            set_position(line, column)
            speak_print(game, message_list[n])
        pause_counter += 1
        if pause_counter == threshold + 1:
            pause_counter = 0
            pause_game(game)


def print_options(game, option_list):
    # Prints options to option box.
    # Lines that exceed text height
    # move into a second column.
    box = get_inner(game).get("options")
    height = box.get("text_height")
    width = box.get("text_width")
    line = box.get("start")
    left = box.get("text_start")
    right = left + (width // 2)
    set_room_text_color(game, "options")
    fill_box(game, "options")

    for n in range(len(option_list)):
        if n < height:
            set_position(line + n, left)
        else:
            set_position(line + n - height, right)
        print(f"{n+1}) {option_list[n].capitalize()}", end="")

    set_cursor(game, "input")


def print_response(game, message):
    # Writes a message to the response box.
    set_room_text_color(game, "response")
    fill_box(game, "response")
    set_cursor(game, "response")
    print(message, end="", flush=True)


def s_print_response(game, message):
    print_response(game, message)
    pause(game)


def print_title(game):
    # Prints the title centered in the upper most element.
    set_room_text_color(game, "title")
    set_bold()
    ui_text = game.get("ui_text")
    title = ui_text.get("title")
    width = get_width(game)
    set_cursor(game, "title")
    print(title.center(width))
    # resets bold text
    set_color(-1)


def print_info(game):
    set_room_text_color(game, "info")
    turn_count = get_turn_count(game)
    width = get_width(game)
    title = get_room_title(game)
    turn_text = f"Turn {turn_count}"
    padding = width - len(title) - len(turn_text)
    space = padding * " "
    set_cursor(game, "info")
    print(f"{title}{space}{turn_text}")


# User input


def collect_input(game):
    # Allows cursor to remain hidden until game accepting
    # user input.
    # Clears the input box after input is collected.
    show_cursor()
    set_cursor(game, "input")
    response = input()
    response.lower()
    fill_box(game, "input")
    hide_cursor()
    return response


def collect_numeric_input(game, options, prompt):
    # Collects a number from the user
    # Prompts again if not a number or outside of
    # the options range
    # Response is returned -1 for zero index
    while True:
        print_response(game, prompt)
        try:
            response = int(collect_input(game))
        except ValueError:
            print_response(game, "Numbers Only")
            pause(game)
        else:
            if response not in range(1, len(options) + 1):
                print_response(game, "Unknown Option")
                pause(game)
            else:
                return response - 1


# Text processing


def print_dialogue(game, text):
    # Takes text and splits it by newline
    # Passes that block of text to the word wrap
    # Then prints those lines returned
    output = []
    for line in text.splitlines():
        output.extend(word_wrap(game, line))
    print_dialogue_lines(game, output)


def word_wrap(game, text_list):
    # Bootleg implimentation of a word wrap function
    # Takes in block of text and returns a list split
    # to fit max width without dividing words.
    width = get_width(game)
    split_text = text_list.split(" ")
    export = []
    buffer = ""
    for word in range(len(split_text)):
        if len(buffer) + len(split_text[word]) >= width:
            export.append(buffer)
            buffer = ""
        buffer += split_text[word] + " "
    export.append(buffer)
    return export


def s_print_dialogue(game, text):
    print_dialogue(game, text)
    pause(game)


def speak_print(game, message):
    # Prints character by character to simulate
    # conversation.
    speed = get_setting(game, "text_speed")
    for ch in message:
        time.sleep(speed / 1000)
        print(ch, end="", flush=True)


def fill_box(game, box_name, char=" "):
    # fills text space with a character
    # when the character is " " it functions as a clear
    box = get_inner(game).get(box_name)
    height = box.get("text_height")
    line = box.get("start")
    column = box.get("text_start")
    width = box.get("text_width")
    for x in range(height):
        set_position(line + x, column)
        print(char * width, flush=True)
    set_cursor(game, "input")


def fill_box_all(game, char=" "):
    # Loops through inner boxes and fills them
    # with the specified character
    inner = get_inner(game)
    for box in inner:
        fill_box(game, box, char)


# random color options


def rainbow_fill_all(game, char=" "):
    # Fills all inner box text space with
    # multi-colored lines
    inner = get_inner(game)
    for box in inner:
        rainbow_fill(game, box)
    set_cursor(game, "input")


def rainbow_fill(game, box_name, char="*"):
    # Fills entire specified text box with
    # multi-colored lines.
    box = get_inner(game).get(box_name)
    height = box.get("text_height")
    column = box.get("text_start")
    start_line = box.get("start")
    for line in range(height):
        set_position(start_line + line, column)
        print_rainbow_line(game, char)


def print_rainbow_line(game, char):
    # Sets a random color and then prints a single
    # character the width of a text box.
    # Color is reset at the end so subsequent characters
    # use the terminal default
    width = get_width(game)
    for n in range(width):
        set_random_color(game)
        print(char, end="", flush=True)


# helper functions


# boxes
def get_inner(game):
    return game.get("boxes").get("inner")


def get_outer(game):
    return game.get("boxes").get("outer")


def get_border(game):
    return game.get("boxes").get("outer").get("border")


def get_width(game, box_name="title"):
    return get_inner(game).get(box_name).get("text_width")


def get_setting(game, setting):
    return game.get("settings").get(setting)


def set_player(game, key, value):
    game.get("player").update({key: value})


def get_player_value(game, key):
    return game.get("player").get(key)


def get_current_room(game):
    return game.get("rooms").get(get_player_room(game))


def get_room_items(game):
    room_name = get_player_room(game)
    return game.get("rooms").get(room_name).get("item_list")


def get_game_items(game):
    return game.get("items")


def get_item_description(game, item_name):
    return get_game_items(game).get(item_name).get("description")


def get_item_type(game, item_name):
    return get_game_items(game).get(item_name).get("type")


def get_item_consumable(game, item_name):
    return get_game_items(game).get(item_name).get("consumable")


def get_item_consumed_msg(game, item_name):
    return get_game_items(game).get(item_name).get("consumed_msg")


def consume_item(game, item_name):
    remove_player_item(game, item_name)


def get_player_items(game):
    return game.get("player").get("item_list")


def add_player_item(game, item_name):
    get_player_items(game).append(item_name)


def remove_player_item(game, item_name):
    get_player_items(game).remove(item_name)


def add_room_item(game, item_name):
    get_current_room(game).get("item_list").append(item_name)


def remove_room_item(game, item_name):
    get_current_room(game).get("item_list").remove(item_name)


def drop_item(game, item_name):
    remove_player_item(game, item_name)
    add_room_item(game, item_name)


def get_item(game, item_name):
    remove_room_item(game, item_name)
    add_player_item(game, item_name)


def get_item_use_success_msg(game, item_name):
    return get_game_items(game).get(item_name).get("success_msg")


def get_item_use_fail_msg(game, item_name):
    return get_game_items(game).get(item_name).get("use_fail_msg")


def get_item_opens(game, item_name):
    return get_game_items(game).get(item_name).get("opens")


def get_color_schemes(game):
    return game.get("color_schemes")


def get_color_scheme(game):
    scheme = get_current_room(game).get("color_scheme")
    return get_color_schemes(game).get(scheme)


def get_box_colors(game):
    return get_color_scheme(game).get("boxes")


def get_room_text_colors(game):
    return get_color_scheme(game).get("text")


def get_room_text_color(game, box_name):
    return get_room_text_colors(game).get(box_name)


def set_room_text_color(game, box_name):
    set_color(get_room_text_color(game, box_name))


def get_player_room(game):
    return get_player_value(game, "current_room")


def set_start_room(game):
    set_player(game, "current_room", get_player_value(game, "start_room"))


def pause(game):
    time.sleep(get_delay(game))


def get_delay(game):
    return get_setting(game, "ui_delay")


def add_room_exit(game, exits_to):
    exits = get_room_exits(game)
    exits.append(exits_to)


def remove_room_exit(game, exits_to):
    exits = get_room_exits(game)
    if exits_to in exits:
        exits.remove(exits_to)
# navigation


def get_navigation(game):
    return get_player_value(game, "navigation")


def add_to_navigation(game, menu_item):
    get_navigation(game).append(menu_item)


def remove_from_navigation(game):
    return get_navigation(game).pop(-1)


def get_current_navigation(game):
    navigation = get_navigation(game)
    return navigation[-1]


def get_turn_count(game):
    return get_player_value(game, "turn_count")


def increment_turn(game, turns=1):
    set_player(game, "turn_count", get_turn_count(game) + turns)


def set_location(game, room_name):
    set_player(game, "current_room", room_name)

# rooms


def get_room_title(game):
    return get_current_room(game).get("title")


def get_room_exits(game):
    return get_current_room(game).get("exits")


def get_item_list(game):
    return get_current_room(game).get("item_list")


def get_room_description(game):
    return get_current_room(game).get("description")


def get_room_visited(game):
    return get_current_room(game).get("visited")


def set_room_visited(game):
    get_current_room(game).update({"visited": 1})


def get_room_brief(game):
    return get_current_room(game).get("brief")


# Details


def get_room_details(game):
    return get_current_room(game).get("details")


def get_details(game):
    return game.get("details")


def get_detail(game, detail_name):
    return get_details(game).get(detail_name)


def get_detail_name(game, detail):
    return get_detail(game, detail).get("name")


def get_detail_type(game, detail):
    return get_detail(game, detail).get("type")


def get_detail_exits_to(game, detail):
    return get_detail(game, detail).get("exits_to")


def get_detail_visible(game, detail):
    return get_detail(game, detail).get("visible")


def get_detail_display_name(game, detail):
    return get_detail(game, detail).get("display_name")


def get_detail_reward(game, detail):
    return get_detail(game, detail).get("reward")


def get_detail_dialogue(game, detail):
    return get_detail(game, detail).get("dialogue")


def get_detail_description(game, detail):
    return get_detail(game, detail).get("description")


def get_detail_locked(game, detail):
    return get_detail(game, detail).get("locked")


def get_detail_locked_msg(game, detail):
    return get_detail(game, detail).get("locked_msg")


def get_detail_unlocked_msg(game, detail):
    return get_detail(game, detail).get("unlocked_msg")


def get_detail_unlock_msg(game, detail):
    return get_detail(game, detail).get("unlock_msg")


def get_detail_lock_msg(game, detail):
    return get_detail(game, detail).get("lock_msg")


def get_detail_closed(game, detail):
    return get_detail(game, detail).get("closed")


def get_detail_closed_msg(game, detail):
    return get_detail(game, detail).get("closed_msg")


def get_detail_opened_msg(game, detail):
    return get_detail(game, detail).get("opened_msg")


def get_detail_open_msg(game, detail):
    return get_detail(game, detail).get("open_msg")


def get_detail_close_msg(game, detail):
    return get_detail(game, detail).get("close_msg")


# def get_detail_key_type(game, detail):
#     return get_detail(game, detail).get("key_type")


def get_detail_key(game, detail):
    return get_detail(game, detail).get("key")


def get_detail_key_fail_msg(game, detail):
    return get_detail(game, detail).get("key_fail_msg")


def get_detail_key_success(game, detail):
    return get_detail(game, detail).get("key_success")


def get_detail_use_msg(game, detail):
    return get_detail(game, detail).get("use_msg")


def get_detail_use_fail_msg(game, detail):
    return get_detail(game, detail).get("use_fail_msg")


def get_detail_use_success(game, detail):
    return get_detail(game, detail).get("use_success")


def get_detail_success_msg(game, detail):
    return get_detail(game, detail).get("success_msg")


# detail sets and toggles


def set_detail_visible(game, detail):
    get_detail(game, detail).update({"visible": 1})


def set_detail_invisible(game, detail):
    get_detail(game, detail).update({"visible": 0})


def toggle_detail_visible(game, detail):
    state = get_detail_visible(game, detail)
    if state == 0:
        set_detail_visible(game, detail)
    else:
        set_detail_invisible(game, detail)


def set_detail_locked(game, detail):
    get_detail(game, detail).update({"locked": 1})


def set_detail_unlocked(game, detail):
    get_detail(game, detail).update({"locked": 0})


def toggle_detail_locked(game, detail):
    state = get_detail_locked(game, detail)
    if state == 0:
        set_detail_locked(game, detail)
    else:
        set_detail_unlocked(game, detail)


def set_detail_open(game, detail):
    get_detail(game, detail).update({"closed": 0})


def set_detail_closed(game, detail):
    get_detail(game, detail).update({"closed": 1})


def toggle_detail_closed(game, detail):
    state = get_detail_closed
    if state == 1:
        set_detail_open(game, detail)
    else:
        set_detail_closed(game, detail)


# menus


def get_menu(game, menu_name):
    return game.get("menus").get(menu_name)


def get_menu_options(game, menu_name):
    return get_menu(game, menu_name).get("options")


def get_current_menu(game):
    current_nav = get_current_navigation(game)
    return get_menu(game, current_nav)


def get_menu_prompt(game):
    return get_current_menu(game).get("prompt")


def get_menu_nothing(game):
    return get_current_menu(game).get("nothing")


def get_menu_success(game):
    return get_current_menu(game).get("success")


def get_menu_options(game):
    return get_current_menu(game).get("options")
