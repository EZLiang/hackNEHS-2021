import discord
from discord.ext import commands
from random import *
from asyncio import sleep


class BlackJack:
    suits = list("♠♥♣♦")
    ranks = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]

    def __init__(self, ctx, msg=None, reaction=None):
        self.available_cards = []
        for i in BlackJack.suits:
            for j in BlackJack.ranks:
                self.available_cards.append([i, j])
        self.win_string = ""
        self.player_hand = []
        self.alexa_hand = []
        em = discord.Embed()
        self.ctx = ctx
        if msg is None:
            self.msg = await ctx.send(embed=m)
            self.new_game()
        else:
            self.from_message(msg, reaction)

    def get_card(self):
        card = choice(self.available_cards)
        self.available_cards.remove(card)
        return card

    def new_game(self):
        for i in range(2):
            self.player_hand.append(self.get_card())
            self.alexa_hand.append(self.get_card())
        self.do_player()

    def from_message(self, message, reaction):
        self.msg = message
        fields = self.msg.embeds[0].to_dict()
        player_formatted = fields["Player's hand"].split(" ")
        alexa_formatted = fields["Alexa's hand"].split(" ")
        self.player_hand = [i for i in map(lambda x: [x[1], x[0]], player_formatted)]
        self.alexa_hand = [i for i in map(lambda x: [x[1], x[0]], alexa_formatted)]
        for i in self.player_hand:
            self.available_cards.remove(i)
        for i in self.alexa_hand:
            self.available_cards.remove(i)
        self.do_player_response(str(reaction) == "🇦")

    def get_hand_sum(self, hand):
        running_sum = 0
        for i in range(len(hand)):
            card_rank = (hand[i])[1]
            if card_rank == "A":
                running_sum += 1
            elif card_rank == "J" or card_rank == "Q" or card_rank == "K":
                running_sum += 10
            else:
                running_sum += int(card_rank)

        return running_sum

    def check_hand_valid(self, hand):
        if self.get_hand_sum(hand) > 21:
            return "Busted..."
        if self.get_hand_sum(hand) == 21:
            return "Blackjack!"
        if self.get_hand_sum(hand) < 21:
            return "Current Total: " + str(BlackJack.get_hand_sum(hand))

    def update_hands(self):
        player_formatted = " ".join([i for i in map(lambda x: x[1] + x[0], self.player_hand)])
        alexa_formatted = " ".join([i for i in map(lambda x: x[1] + x[0], self.alexa_hand)])
        em = discord.Embed()
        em.add_field(name="Player's hand", value=player_formatted)
        em.add_field(name="Alexa's hand", value=alexa_formatted)
        await self.msg.edit(embed=em)

    def do_player(self):
        self.update_hands()
        self.msg.edit("🇦 to hit, 🇧 to stand")
        await self.msg.add_reaction("🇦")
        await self.msg.add_reaction("🇧")

    def do_player_response(self, hit):
        if hit:
            drawn_card = self.get_card()
            self.player_hand.append(drawn_card)
            await self.ctx.send("Drawn Card:" + drawn_card[1] + drawn_card[0])
            self.update_hands()
            if self.check_hand_valid(self.player_hand) == "Busted...":
                self.win_string = "The computer wins! Better luck next time..."
                self.endgame()
            elif self.check_hand_valid(self.player_hand) == "Blackjack!":
                self.win_string = "You won! Nice job!"
                self.endgame()
            else:
                self.do_player()
        else:
            self.handle_alexa()

    def handle_alexa(self):
        sleep(0.5)
        self.update_hands()
        if self.get_hand_sum(self.alexa_hand) < 17:
            randomizer = randint(1, 12)
            if randomizer == 12:
                await self.ctx.send("Stand")
            else:
                await self.ctx.send("Hit")
                drawn_card = self.get_card()
                self.alexa_hand.append(drawn_card)
                await self.ctx.send("Drawn Card:" + drawn_card[1] + drawn_card[0])
        elif self.get_hand_sum(self.alexa_hand) >= 17:
            randomizer = randint(1, 20)
            if randomizer == 20:
                await self.ctx.send("Stand")
            else:
                await self.ctx.send("Hit")
                drawn_card = self.get_card()
                self.alexa_hand.append(drawn_card)
                await self.ctx.send("Drawn Card:" + drawn_card[1] + drawn_card[0])
        if self.check_hand_valid(self.alexa_hand) == "Busted...":
            self.win_string = "The player wins! The computer should get smarter..."
            self.endgame()
        elif self.check_hand_valid(self.alexa_hand) == "Blackjack!":
            self.win_string = "The computer won! Better luck next time..."
            self.endgame()
        else:
            self.handle_alexa()

    def endgame(self):
        self.update_hands()
        sleep(0.5)
        await self.ctx.send(self.win_string)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.available_cards = []
        self.player_hand = []
        self.alexa_hand = []

    @commands.command(name="blackjack")
    async def bj(self, ctx):
        BlackJack(ctx)

    @commands.Cog.listener
    async def on_reaction_add(self, reaction):
        BlackJack(reaction.message.channel, reaction.message, reaction.emoji)
