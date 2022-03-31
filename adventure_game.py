__author__ = "David Cooper"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "David Cooper"
__email__ = "exaptation@gmail.com"
__status__ = "Development"

import time
import os
import random

# import random
import gameboard
import json
import ui


def pre_check(game):
    # Game requires space in order to render correctly.
    # This checks the size of the terminal it is run in and
    # informs the user to expand the size of the terminal
    # If it is too small and exits gracefully.
    ui.clear_screen()
    columns = os.get_terminal_size().columns
    lines = os.get_terminal_size().lines
    border = ui.get_border(game)
    min_columns = border.get("width")
    min_lines = border.get("height")
    ui_text = game.get("ui_text")
    loading_message(game, ui_text.get("loading1"))
    print("Terminal window detected as:")
    print(f"{columns} columns by {lines} lines")
    if columns < min_columns or lines < min_lines:
        ui.pause(game)
        print("Optimal terminal size:")
        print(f"{min_columns} columns by {min_lines} lines")
        ui.pause(game)
        print("Adjust the terminal window")
        print("and restart the program")
        ui.pause(game)
        exit()
    else:
        loading_message(game, ui_text.get("loading2"))
        ui.clear_screen()


def loading_message(game, messages):
    # Prints the messages slowly to build suspense.
    for message in messages:
        print(message)
        ui.pause(game)


def choose_name(game):
    # Prompts the user for their name and stores it.
    # Minimum and maximum values are set in the game settings.
    name = ""
    settings = game.get("settings")
    ui_text = game.get("ui_text")
    max_name = settings.get("max_name")
    min_name = settings.get("min_name")
    while len(name) < min_name or len(name) > max_name:
        ui.print_response(game, ui_text.get("enter_name"))
        name = ui.collect_input(game)
        if len(name) > max_name:
            ui.s_print_response(game, ui_text.get("too_long"))
            ui.print_response(game, ui_text.get("max_name"))
        elif len(name) < min_name:
            ui.s_print_response(game, ui_text.get("too_short"))
            ui.print_response(game, ui_text.get("min_name"))
        else:
            name.capitalize()
            ui.s_print_response(game, f"""{name}{ui_text.get("scribe")}""")
            ui.set_player(game, "name", name)
        ui.pause(game)


def exit_game(game):
    # Show cursor
    ui.show_cursor()
    # Reset color
    ui.set_color(-1)
    # Set cursor outside of game display
    ui.set_cursor(game, "exit")
    exit()


def look(game):
    ui.print_response(game, "Looking")
    print_room_full(game)
    print_room_items(game)


def get_menu(game):
    items = ui.get_room_items(game)
    prompt = ui.get_menu_prompt(game)
    nothing = ui.get_menu_nothing(game)
    menu_options = ui.get_menu_options(game)
    if not items:
        ui.s_print_response(game, nothing)
    else:
        options = items + menu_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            item_name = items[response]
            ui.s_print_response(game, f"{item_name.capitalize()} Acquired!")
            ui.get_item(game, item_name)
    back(game)


def move_menu(game):
    # Gets list of exits from room and presents it as options
    # Changes the current room on player.
    prompt = ui.get_menu_prompt(game)
    nothing = ui.get_menu_nothing(game)
    success = ui.get_menu_success(game)
    exits = ui.get_room_exits(game)
    menu_options = ui.get_menu_options(game)
    if not exits:
        ui.s_print_response(game, nothing)
    else:
        options = exits + menu_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            room_name = options[response]
            ui.set_location(game, room_name)
            ui.print_response(game, f"{room_name.capitalize()} Selected!")
            ui.pause(game)
            ui.s_print_dialogue(game, f"{success}{room_name}.")
            # Increment turn count
            ui.increment_turn(game)
    back(game)


def interact_menu(game):
    # ui.s_print_response(game, "INTERACT MENU")
    prompt = ui.get_menu_prompt(game)
    nothing = ui.get_menu_nothing(game)
    interact_options = ui.get_menu_options(game)
    details = ui.get_room_details(game)
    visible_details = ""
    for detail in details:
        visible = ui.get_detail_visible(game, detail)
        if visible:
            visible_details += detail
    menu_options = ui.get_menu_options(game)
    if not visible_details:
        ui.s_print_response(game, nothing)
    else:
        options = details + interact_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            detail_name = options[response]
            ui.print_response(game, f"{detail_name.capitalize()} Selected!")
            interact_detail(game, detail_name)
            ui.pause(game)
    back(game)


def interact_detail(game, detail):
    use_msg = ui.get_detail_use_msg(game, detail)
    ui.s_print_dialogue(game, use_msg)
    locked = ui.get_detail_locked(game, detail)
    exits_to = ui.get_detail_exits_to(game, detail)
    if locked == 1:
        locked_msg = ui.get_detail_locked_msg(game, detail)
        ui.s_print_dialogue(game, locked_msg)
    else:
        closed = ui.get_detail_closed(game, detail)
        if closed == 1:
            open_msg = ui.get_detail_open_msg(game, detail)
            ui.s_print_dialogue(game, open_msg)
            ui.set_detail_open(game, detail)
            detail_type = ui.get_detail_type(game, detail)
            if detail_type == "exit":
                exits_to = ui.get_detail_exits_to(game, detail)
                ui.add_room_exit(game, exits_to)
                ui.print_response(game, f"{exits_to.capitalize()} discovered!")
            if detail_type == "reward":
                reward = ui.get_detail_reward(game, detail)
                ui.add_player_item(game, reward)
                ui.print_response(game, f"{reward.capitalize()} attained!")
        elif closed == 0:
            close_msg = ui.get_detail_close_msg(game, detail)
            ui.s_print_dialogue(game, close_msg)
            ui.set_detail_closed(game, detail)
            ui.remove_room_exit(game, exits_to)


def drop_menu(game):
    player_items = ui.get_player_items(game)
    menu_options = ui.get_menu_options(game)
    prompt = ui.get_menu_prompt(game)
    nothing = ui.get_menu_nothing(game)
    if not player_items:
        ui.s_print_response(game, nothing)
    else:
        options = player_items + menu_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            item_name = options[response]
            ui.s_print_response(game, f"{item_name.capitalize()} Dropped!")
            ui.drop_item(game, item_name)
    back(game)


def inspect_menu(game):
    prompt = ui.get_menu_prompt(game)
    details = ui.get_room_details(game)
    nothing = ui.get_menu_nothing(game)
    menu_options = ui.get_menu_options(game)
    if not details:
        ui.s_print_response(game, nothing)
    else:
        options = details + menu_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            detail_name = options[response]
            inspect_detail(game, options[response])
            # ui.s_print_dialogue(game, f"{item_name} inspected!")
            description = ui.get_detail_description(game, detail_name)
            # ui.print_dialogue(game, description)

    back(game)


def examine_item(game):
    player_items = ui.get_player_items(game)
    menu_options = ui.get_menu_options(game)
    prompt = ui.get_menu_prompt(game)
    nothing = ui.get_menu_nothing(game)
    if not player_items:
        ui.s_print_response(game, nothing)
    else:
        options = player_items + menu_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            item_name = options[response]
            description = ui.get_item_description(game, item_name)
            ui.s_print_dialogue(game, description)
    back(game)


def inspect_detail(game, detail):
    description = ui.get_detail_description(game, detail)
    locked = ui.get_detail_locked(game, detail)
    closed = ui.get_detail_closed(game, detail)
    message = ""
    if locked:
        locked_status = ui.get_detail_locked_msg(game, detail)
    else:
        locked_status = ui.get_detail_unlocked_msg(game, detail)
    if closed:
        closed_status = ui.get_detail_closed_msg(game, detail)
    else:
        closed_status = ui.get_detail_opened_msg(game, detail)
    message = f"{description}\n{locked_status}\n{closed_status}"
    ui.s_print_dialogue(game, message)


def use_menu(game):
    player_items = ui.get_player_items(game)
    menu_options = ui.get_menu_options(game)
    prompt = ui.get_menu_prompt(game)
    nothing = ui.get_menu_nothing(game)
    if not player_items:
        ui.s_print_response(game, nothing)
    else:
        options = player_items + menu_options
        ui.print_options(game, options)
        response = ui.collect_numeric_input(game, options, prompt)
        if response != len(options) - 1:
            item_name = options[response]
            use_item(game, item_name)
    back(game)


def use_item(game, item_name):
    item_type = ui.get_item_type(game, item_name)
    match = 0
    if item_type == "key":
        details = ui.get_room_details(game)
        for detail in details:
            detail_key = ui.get_detail_key(game, detail)
            if detail_key == item_name:
                match = 1
                success_msg = ui.get_item_use_success_msg(game, item_name)
                ui.s_print_dialogue(game, success_msg)
                ui.toggle_detail_locked(game, detail)
        if match == 0:
            use_fail_msg = ui.get_item_use_fail_msg(game, item_name)
            ui.s_print_dialogue(game, use_fail_msg)
    consumable = ui.get_item_consumable(game, item_name)
    if consumable == 1:
        consume(game, item_name)
    # elif item_type == ""
    back(game)


def consume(game, item_name):
    consumed_msg = ui.get_item_consumed_msg(game, item_name)
    ui.print_dialogue(game, consumed_msg)
    ui.consume_item(game, item_name)
    ui.pause_game(game)
    if item_name == "strange berries":
        ui.eat_strange_berries(game)


def inventory_menu(game):
    prompt = ui.get_menu_prompt(game)
    options = ui.get_menu_options(game)
    ui.print_options(game, options)
    response = ui.collect_numeric_input(game, options, prompt)
    # ui.s_print_dialogue(game, options[response])
    ui.add_to_navigation(game, options[response])

    # Make options menu of details in room4
    # Collect numeric input
    # Show details which can activate
    # the detail


def settings_menu(game):
    ui.s_print_response(game, "SETTINGS MENU")
    back(game)


def user_menu(game):
    prompt = ui.get_menu_prompt(game)
    options = ui.get_menu_options(game)
    ui.print_response(game, prompt)
    ui.print_options(game, options)
    response = ui.collect_numeric_input(game, options, prompt)
    if response == 0:
        look(game)
    else:
        ui.add_to_navigation(game, options[response])
    show_menu(game)


def show_menu(game):
    # debugging code
    # ui.set_cursor(game, "exit")
    # print("Navigation ", ui.get_navigation(game))
    menu = ui.get_current_navigation(game)
    if menu == "user":
        user_menu(game)
    elif menu == "inspect":
        inspect_menu(game)
    elif menu == "interact":
        interact_menu(game)
    elif menu == "get":
        get_menu(game)
    elif menu == "move":
        move_menu(game)
    elif menu == "inventory":
        inventory_menu(game)
    elif menu == "settings":
        settings_menu(game)
    elif menu == "quit":
        exit_game(game)
    elif menu == "examine":
        examine_item(game)
    elif menu == "drop":
        drop_menu(game)
    elif menu == "use":
        use_menu(game)
    elif menu == "back":
        back(game, 2)
        show_menu(game)
    else:
        print("MENU FAIL!")
        ui.pause(game)
        exit_game(game)


def back(game, num=1):
    for x in range(num):
        ui.remove_from_navigation(game)


def print_room_brief(game):
    ui.s_print_dialogue(game, ui.get_room_brief(game))


def print_room_description(game):
    ui.s_print_dialogue(game, ui.get_room_description(game))


def print_room_details(game):
    details = ui.get_room_details(game)
    for detail in details:
        if ui.get_detail_visible(game, detail):
            ui.s_print_dialogue(game, ui.get_detail_dialogue(game, detail))


def print_room_full(game):
    print_room_brief(game)
    print_room_description(game)
    print_room_details(game)
    print_room_items(game)


def print_room(game):
    room = ui.get_current_room(game)
    if room != "main":
        if ui.get_room_visited(game) == 0:
            print_room_full(game)
            ui.set_room_visited(game)


def print_room_items(game):
    title = ui.get_room_title(game)
    item_list = ui.get_item_list(game)
    items = ui.get_game_items(game)
    message = []
    if item_list:
        room_item_text = f"In {title} you see:\n"
        message.append(room_item_text)
        for item in item_list:
            description = ui.get_item_description(game, item)
            message.append(description)
        ui.print_dialogue_lines(game, message)


def draw_room(game):
    # Gets the color codes from the room dictionary
    # and draws the box
    scheme = ui.get_box_colors(game)
    for box in scheme:
        ui.set_color(scheme.get(box))
        if box != "border":
            ui.draw_inner(game, box)
        else:
            ui.draw_border(game)


def display_room(game):
    # Displays the room.
    # The first time the room displayed
    # print brief and long description.
    # Mark room as "visited" and only print brief
    draw_room(game)
    ui.print_title(game)
    ui.print_info(game)
    print_room(game)


def game_loop(game):
    display_room(game)
    choose_name(game)
    ui.set_location(game, "river")
    while True:
        ui.clear_screen()
        ui.print_title(game)
        display_room(game)
        show_menu(game)


def start_game():
    ui.clear_screen()
    ui.hide_cursor()
    game = gameboard.build_game()
    # pre_check(game)
    game_loop(game)
    exit_game(game)
    # print(json.dumps(game, indent=4))


start_game()
