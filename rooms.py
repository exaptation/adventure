# All of the information necessary to describe a room
# are contained in this file.
# Exits link the rooms together.


def build_rooms():
    rooms = {
        "main": {
            "title": "Main Menu",
            "brief": (
                "Hello brave ACCENTURER!\n"
                "A brief but colorful adventure await you.\n\n"
                "The last thing you remember clearly you were hanging out "
                "with your wizard friend Otto the Enchanter at the tavern by "
                "the river. He picked up a glass of mead, tilted his head "
                "back, finished his cup, hicupped loudly and then said, "
                """\n\n"I bet you I can talk those giants into giving me"""
                " that magic apple they found and I'm sure the gnomes "
                """won't mind one little bit."\n\n"""
                "Then you remember the sound of angry gnomes, poorly "
                "pronounced magic incantations, "
                "and then the thunderous yell of a giant.\n\n"
                "Tell me your name that the bards can sing your tales for "
                "eons to come!\n\nOr at least what to write on the "
                """\n"Have you seen this brave adventurer?" poster.\n\n"""
            ),
            "description": "",
            "item_list": [],
            "exits": ["river"],
            "details": [],
            "visited": 0,
            "color_scheme": "default",
        },
        "forest": {
            "title": "The Enchanted Forest",
            "brief": "You are standing in an enchanted forest.\n",
            "description": (
                "The trees seem to be watching you or mocking your "
                "predicament.\nYou can't quite tell.\n"
                "Bright beams of light shine down through the canopy."
            ),
            "item_list": ["strange berries"],
            "exits": ["cave", "river", "hut"],
            "visited": 0,
            "details": [],
            "color_scheme": "green",
        },
        "hut": {
            "title": "The Magical Hut",
            "brief": "You are standing in a colorful hut",
            "description": (
                "The continual beat of a mystic bard emminates "
                "from a pulsing stone.\n"
                "Rays of multi-colored light illuminate "
                "and dance about the room."
            ),
            "item_list": [],
            "exits": ["forest"],
            "visited": 0,
            "details": ["groovy witch"],
            "color_scheme": "neon",
        },
        "cave": {
            "title": "The Dark Cave",
            "brief": "You are standing in a dark cave.\n",
            "description": (
                "It's totally dark.\n"
                "You almost can't see your hand in front of your "
                "face."
            ),
            "item_list": [],
            "exits": ["forest"],
            "visited": 0,
            "color_scheme": "purple",
            "details": ["door"],
        },
        "river": {
            "title": "The Magical River",
            "brief": "You're standing by an immense river.\n",
            "description": (
                "A rapidly flowing river dashes violently "
                "on rocks.\n"
                "It in no way looks safe to swim in.\n"
            ),
            "item_list": ["note"],
            "exits": ["forest"],
            "visited": 0,
            "color_scheme": "blue",
            "details": "",
        },
        "end": {
            "title": "WINNER!!!!!!!!!!!!!!!!!!!!",
            "brief": "You have won the game!!!!",
            "description": (
                "This is where more content goes when you "
                "have not suddenly started a new job.\n\n"
                "The game will automatically start again "
                "after you enter your name.\n\n"
                "Press quit to exit."
            ),
            "item_list": [],
            "exits": [],
            "visited": 0,
            "color_scheme": "default",
            "details": "",
        }
    }
    return rooms


def build_details():
    details = {
        "door": {
            "name": "oaken door",
            "type": "exit",
            "exits_to": "end",
            "visible": 1,
            "display_name": "A large oak door",
            "dialogue": "Against the cave wall there is a door.",
            "description": ("You see a large ornate oak door with"
                            " a brass lock."),
            "use_msg": ("You appreciate the heavy feel of genuine "
                        "wood as you grab the door."),
            "key": "silver key",
            "locked": 1,
            "locked_msg": ("However, the door is locked and no amount"
                           " of force will open it."),
            "unlocked_msg": "The door is unlocked",
            "unlock_msg": "With a satisfying click, you unlock the door",
            "lock_msg": "After a lot of fiddeling you lock the door",
            "closed": 1,
            "closed_msg": "The door is closed",
            "opened_msg": "The door is open",
            "close_msg": "With a satisfying thud, you close the door",
            "open_msg": ("It seems firmly shut but sufficient force "
                         "opens the door and reveals a path to the hut.\n"
                         "You think you hear Otto."),
        },
        "groovy witch": {
            "name": "groovy witch",
            "type": "reward",
            "reward": "silver key",
            "visible": 1,
            "display_name": "The grooviest witch",
            "dialogue": ("In the hut a woman dressed in shimmering robes "
                         "stirs a metal cauldron in time with the music."),
            "description": ("Wearing a prismatic robe and singing to herself\n"
                            "this could only be the Groovey witch."),
            "use_msg": ("You party with the Groovey witch!"),
            "key": "strange berries",
            "locked": 1,
            "locked_msg": ("""She says, "I really could use some berries """
                           """to make this potion.\n"""
                           """I hear they grow in the woods."""),
            "unlocked_msg": "The groovey witch seems to be vibing.",
            "unlock_msg": ("You offer the strange berries to the witch.\n"
                           "She takes them, mixes them in her cauldron and "
                           "a puff of pink smoke fills the air."),
            "lock_msg": "You offer even more strange berries to the witch.",
            "closed": 1,
            "closed_msg": "",
            "opened_msg": "",
            "close_msg": "",
            "open_msg": ("What a great day. Here's a small trinket to "
                         "remember it by!\nThanks a lot. You're alright "
                         "in my spellbook despite what people say.\n"
                         "You get the silver key!")
        },
    }
    return details


def build_items():
    items = {
        "note": {
            "description": "A note from a friend",
            "consumable": 1,
            "consumed_msg": (
                "You open the note and read it\n"
                "It's and IOU from a Otto the Enchanter\n"
                'It says "Sorry for all of the problems I caused'
                " and your massive bar tab.\n"
                "This IOU good for one game of elven bowling "
                "any day that there is a pending lunar eclipse "
                "and no giants claim to be the king of the realm.\n"
                "Good luck getting home. Look for a door.\n"
                "The note then busts into flames..."),
        },
        "apple": {
            "description": "A perfect red apple",
            "consumable": 1,
            "consumed_msg": ("You eat the apple.\n"
                             "It was delcious but probably not worth"
                             " all this trouble!"),
        },
        "silver key": {
            "name": "silver key",
            "type": "key",
            "opens": "door",
            "consumable": 0,
            "get_msg": "You pick up the silver key",
            "drop_msg": "You put down the silver key",
            "description": "A tarnished silver key",
            "use_fail_msg": "There is nothing to unlock",
            "success_msg": ("You put the key in the lock and turn it\n"
                            "with a metalic click the lock opens!")},
        "strange berries": {
            "name": "strange berries",
            "type": "key",
            "opens": "groovy witch",
            "consumable": 1,
            "get_msg": "The strange berries glow with a pale blue light",
            "drop_msg": ("You put the berries on ground where they emit "
                         "a strange blue light"),
            "description": "Strange glowing berries",
            "use_fail_msg": "You're certain these should ever be consumed.",
            "success_msg": ("You offer the strange berries and the witches "
                            """eyes light up\n"Now this is what I'm talking """
                            """about!", she exclaims.\n"If you get lost be """
                            'sure to meet back up here." she says knowingly.'),
            "consumed_msg": "Maybe this was not a good idea?"
        },
    }

    return items
