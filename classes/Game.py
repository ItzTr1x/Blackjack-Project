from classes.GUI import GUI
from classes.GameData import GameData
from classes.Deck import Deck
from classes.Hand import Hand


class Game:

    stats = None

    def __init__(self):
        self.widgets = {}
        self.table = {}
        self.window = GUI()
        self.frames = {}
        self.window.create_frame("title_frame", 0)
        self.window.create_frame("cards_frame", 1)
        self.window.create_frame("state_frame", 2)
        self.stats = GameData()
        self.player = 0
        self.dealer = 0
        self.start()
        self.window.loop()

    # Game startup
    def start(self):
        self.player_name = self.window.getVariable("string")
        self.widgets["name_label"] = self.window.addLabel(
            "title_frame", "Enter Your Name:", row=1, col=0
        )
        self.widgets["name_input"] = self.window.addTextInput(
            "title_frame", self.player_name, row=1, col=1
        )
        self.widgets["name_button"] = self.window.addSubmit(
            "title_frame",
            "   Lets Play   ",
            command=self.catchPlayer,
            row=1,
            col=2,
            width=1,
        )

    def catchPlayer(self):
        self.players_name = self.player_name.get()
        self.window.kill(self.widgets.pop("name_label"))
        self.window.kill(self.widgets.pop("name_input"))
        self.window.kill(self.widgets.pop("name_button"))
        self.window.addText(
            "title_frame",
            "Welcome to Blackjack, " + self.players_name,
            row=1,
            col=0,
            width=5,
        )
        self.play_menu()

    def play_menu(self):
        self.stats_load()
        for element in self.table:
            self.window.kill(element)
        self.table = {}
        if "play_button" in self.widgets:
            self.window.kill(self.widgets.pop("play_button"))
        if "end_button" in self.widgets:
            self.window.kill(self.widgets.pop("end_button"))
        if "dealer_value" in self.widgets:
            self.window.kill(self.widgets.pop("dealer_value"))

        if self.player:
            for cardx in self.player.cards:
                self.window.kill(self.widgets.pop(cardx.name))
        if self.dealer:
            for cardx in self.dealer.cards:
                self.window.kill(self.widgets.pop(cardx.name))

        self.widgets["quit_button"] = self.window.addSubmit(
            "title_frame", "   Quit   ", command=self.close_game, row=2, col=10, width=2
        )

        self.play_hand()

    def stats_load(self):
        self.stats.load()
        if "stats" in self.widgets:
                self.window.kill(self.widgets.pop("stats"))
        stats = f"Your Stats: Wins: {self.stats.stats['wins']}, Losses: {self.stats.stats['losses']}, Total Games: {self.stats.stats['wins']  + self.stats.stats['losses']}"
        self.widgets["stats"] = self.window.addText("title_frame", stats, row=2, col=0, width=7)
        self.widgets["reset_stats"] = self.window.addSubmit(
            "title_frame",
            "   Reset Stats   ",
            command=self.stats_reset,
            row=2,
            col=8,
            width=2,
        )

    def stats_reset(self):
        self.stats.reset()
        self.stats.display()
        self.stats.save()

    # Deal out cards to player and dealer
    def play_hand(self):
        self.deck = Deck()
        self.player = Hand(self.window, False)
        self.dealer = Hand(self.window, True)
        this_card = self.player.add(self.deck.pop_deck(), True)
        self.widgets[self.player.cards[-1].name] = this_card
        this_card = self.dealer.add(self.deck.pop_deck(), False)
        self.widgets[self.dealer.cards[-1].name] = this_card
        this_card = self.player.add(self.deck.pop_deck(), True)
        self.widgets[self.player.cards[-1].name] = this_card
        this_card = self.dealer.add(self.deck.pop_deck(), True)
        self.widgets[self.dealer.cards[-1].name] = this_card
        self.end_game = False
        self.players_turn()

    # Get player action (hit or stand)
    def players_turn(self):
        self.window.addText(
            "cards_frame",
            "Player Value: " + str(self.player.value),
            row=2,
            col=0,
            width=5,
        )

        if "game_state" in self.widgets:
            self.window.kill(self.widgets.pop("game_state"))

        self.widgets["players_turn"] = self.window.addText(
            "state_frame", "What would you like to do?", row=0, col=0, width=5
        )
        self.widgets["hit_button"] = self.window.addSubmit(
            "state_frame", "   Hit Me   ", command=self.hit_me, row=11, col=1, width=2
        )
        self.widgets["stand_button"] = self.window.addSubmit(
            "state_frame",
            "   Stand   ",
            command=self.dealers_turn,
            row=11,
            col=3,
            width=2,
        )
        self.game_state(player_turn=True)

    def hit_me(self):
        this_card = self.player.add(self.deck.pop_deck(), True)
        self.widgets[self.player.cards[-1].name] = this_card
        self.window.addText(
            "cards_frame",
            "Player Value: " + str(self.player.value),
            row=2,
            col=0,
            width=5,
        )
        self.game_state(player_turn=True)

    def dealers_turn(self):
        # if not self.end_game:
        self.dealer.show_face(self.dealer.cards[0], 0)
        if "dealer_value" in self.widgets:
            self.window.kill(self.widgets.pop("dealer_value"))
        self.widgets["dealer_value"] = self.window.addText(
            "cards_frame",
            "Dealer Value: " + str(self.dealer.value),
            row=5,
            col=0,
            width=5,
        )
        while self.dealer.value < 17:
            this_card = self.dealer.add(self.deck.pop_deck(), True)
            self.widgets[self.dealer.cards[-1].name] = this_card
            if "dealer_value" in self.widgets:
                self.window.kill(self.widgets.pop("dealer_value"))
            self.widgets["dealer_value"] = self.window.addText(
                "cards_frame",
                "Dealer Value: " + str(self.dealer.value),
                row=5,
                col=0,
                width=5,
            )
        self.game_state(player_turn=False)

    def game_state(self, player_turn):
        if player_turn:
            if self.player.value == 21:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))
                self.widgets["game_state"] = self.window.addText(
                    "state_frame", "You got Blackjack! You Win!", row=0, col=0, width=5
                )
                self.stats.increment("wins")
                self.stats.save()
                self.end_game = True
            elif len(self.player.cards) == 5 and self.player.value <= 21:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))
                self.widgets["game_state"] = self.window.addText(
                    "state_frame",
                    "You got a Five-Card Charlie! You Win!",
                    row=0,
                    col=0,
                    width=5,
                )
                self.stats.increment("wins")
                self.stats.save()
                self.end_game = True
            elif self.player.value > 21:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))
                self.widgets["game_state"] = self.window.addText(
                    "state_frame", "You busted! You lose!", row=0, col=0, width=5
                )
                self.stats.increment("losses")
                self.stats.save()
                self.end_game = True
            else:
                self.end_game = False
        else:
            if self.dealer.value > 21:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))
                self.widgets["game_state"] = self.window.addText(
                    "state_frame", "The dealer busted! You win!", row=0, col=0, width=5
                )
                self.stats.increment("wins")
                self.stats.save()
                self.end_game = True
            elif self.dealer.value > self.player.value:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))
                self.widgets["game_state"] = self.window.addText(
                    "state_frame", "You lose! Too bad...", row=0, col=0, width=5
                )
                self.stats.increment("losses")
                self.stats.save()
                self.end_game = True
            elif self.player.value == self.dealer.value:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))
                
                self.widgets["game_state"] = self.window.addText(
                    "state_frame", "It's a tie! Nobody wins!", row=0, col=0, width=5
                )
                self.stats.save()
                self.end_game = True
            else:
                if "players_turn" in self.widgets:
                    self.window.kill(self.widgets.pop("players_turn"))

                self.widgets["game_state"] = self.window.addText(
                    "state_frame", "Congratulations! You win!", row=0, col=0, width=5
                )
                self.stats.increment("wins")
                self.stats.save()
                self.end_game = True

        if self.end_game:
            self.play_again()

    def play_again(self):
        self.window.kill(self.widgets.pop("hit_button"))
        self.window.kill(self.widgets.pop("stand_button"))
        self.widgets["play_button"] = self.window.addSubmit(
            "state_frame",
            "   Play Again   ",
            command=self.play_menu,
            row=1,
            col=1,
            width=2,
        )
        self.widgets["end_button"] = self.window.addSubmit(
            "state_frame", "   Quit   ", command=self.close_game, row=1, col=3, width=2
        )

    def close_game(self):
        self.window.leave()
