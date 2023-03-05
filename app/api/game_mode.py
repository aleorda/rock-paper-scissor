from dataclasses import dataclass


@dataclass
class Action:
    code: str
    name: str
    strong_to: list[str]

    def beats(self, other):
        return other in self.strong_to


@dataclass
class GameMode:
    code: str
    name: str
    actions: list[Action]
    description: str


class GameModes:
    def __init__(self):
        self.modes = {}

    def register(self, game_mode):
        if game_mode.code in self.modes:
            raise ValueError(f"Game mode {game_mode.code} already registered")
        self.modes[game_mode.code] = game_mode
        return game_mode

    def __getitem__(self, key):
        return self.modes.get(key)

    def __len__(self):
        return len(self.modes)


def calculate_result(player_action, computer_action, game_mode):
    if player_action not in [action.code for action in game_mode.actions]:
        return "invalid"

    if player_action == computer_action.code:
        return "draw"
    elif computer_action.beats(player_action):
        return "lose"
    else:
        return "win"


game_modes = GameModes()
game_modes.register(
    GameMode(
        code="classic",
        name="Classic",
        actions=[
            Action(code="rock", name="Rock", strong_to=["scissors"]),
            Action(code="paper", name="Paper", strong_to=["rock"]),
            Action(code="scissors", name="Scissors", strong_to=["paper"]),
        ],
        description="""
        -> Rock crushes Scissors (✊ > ✌)
        -> Scissors cuts Paper (✌ > ✋)
        -> Paper covers Rock (✋ > ✊)
        """,
    )
)

game_modes.register(
    GameMode(
        code="the_big_bang_theory",
        name="The Big Bang Theory",
        actions=[
            Action(code="rock", name="Rock", strong_to=["scissors", "lizard"]),
            Action(code="paper", name="Paper", strong_to=["rock", "spock"]),
            Action(code="scissors", name="Scissors", strong_to=["paper", "lizard"]),
            Action(code="lizard", name="Lizard", strong_to=["spock", "paper"]),
            Action(code="spock", name="Spock", strong_to=["rock", "scissors"]),
        ],
        description="""
        -> Scissors cuts Paper (✌ > ✋)
        -> Paper covers Rock (✋ > ✊)
        -> Rock crushes Lizard (✊ > 🦎)
        -> Lizard poisons Spock (🦎 > 🖖)
        -> Spock smashes Scissors (🖖 > ✌)
        -> Scissors decapitates Lizard (✌ > 🦎)
        -> Lizard eats Paper (🦎 > ✋)
        -> Paper disproves Spock (✋ > 🖖)
        -> Spock vaporizes Rock (🖖 > ✊)
        -> Rock crushes Scissors (✊ > ✌)
        """,
    )
)
