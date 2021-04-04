import discord
from discord.ext import commands
from random import *
from asyncio import sleep


class BlackJack:
    suits = list("♠♥♣♦")
    ranks = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]

    def __init__(self, ctx, msg=None):
        self.available_cards = []
        for i in BlackJack.suits:
            for j in BlackJack.ranks:
                self.available_cards.append([i, j])
        shuffle(self.available_cards)
        self.win_string = ""
        self.player_hand = []
        self.alexa_hand = []
        self.ctx = ctx
        if msg is None:
            self.msg = None
        else:
            self.from_message(msg)

    def get_card(self):
        return self.available_cards.pop()

    async def new_game(self):
        self.msg = await self.ctx.send(embed=discord.Embed())
        for i in range(2):
            self.player_hand.append(self.get_card())
            self.alexa_hand.append(self.get_card())
        await self.do_player()

    def from_message(self, message):
        self.msg = message
        fields = self.msg.embeds[0].to_dict()["fields"]
        player_formatted = fields[0]["value"].split(" ")
        alexa_formatted = fields[1]["value"].split(" ")
        self.player_hand = [i for i in map(lambda x: [x[1], x[0]], player_formatted)]
        self.alexa_hand = [i for i in map(lambda x: [x[1], x[0]], alexa_formatted)]
        for i in self.player_hand:
            try:
                self.available_cards.remove(i)
            except:
                ...
        for i in self.alexa_hand:
            try:
                self.available_cards.remove(i)
            except:
                ...

    def get_hand_sum(self, hand):
        running_sum = 0
        for i in hand:
            card_rank = i[1]
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
        if self.get_hand_sum(hand) == 11 and self.has_ace(hand):
            return "Blackjack!"
        if self.get_hand_sum(hand) < 11 and self.has_ace(hand):
            return "Current Total: " + str(self.get_hand_sum(hand)) + " or " + str(10 + self.get_hand_sum(hand))
        if self.get_hand_sum(hand) < 21:
            return "Current Total: " + str(self.get_hand_sum(hand))

    def has_ace(self, hand):
        for i in hand:
            if i[1] == "A":
                return True
        return False

    async def update_hands(self):
        player_formatted = " ".join([i for i in map(lambda x: x[1] + x[0], self.player_hand)])
        alexa_formatted = " ".join([i for i in map(lambda x: x[1] + x[0], self.alexa_hand)])
        em = discord.Embed()
        em.add_field(name="Player's hand", value=player_formatted)
        em.add_field(name="Alexa's hand", value=alexa_formatted)
        await self.msg.edit(embed=em)

    async def do_player(self):
        await self.update_hands()
        await self.msg.edit(content="🇦 to hit, 🇧 to stand")
        await self.msg.add_reaction("🇦")
        await self.msg.add_reaction("🇧")

    async def do_player_response(self, hit):
        await self.msg.edit(content=None)
        await self.msg.clear_reactions()
        if hit:
            drawn_card = self.get_card()
            self.player_hand.append(drawn_card)
            await self.ctx.send("Drawn Card: " + drawn_card[1] + drawn_card[0])
            await self.update_hands()
            await self.ctx.send(self.check_hand_valid(self.player_hand))
            if self.check_hand_valid(self.player_hand) == "Busted...":
                self.win_string = "The computer wins! Better luck next time..."
                await self.endgame()
            elif self.check_hand_valid(self.player_hand) == "Blackjack!":
                self.win_string = "You won! Nice job!"
                await self.endgame()
            else:
                await sleep(0.5)
                await self.do_player()
        else:
            await self.handle_alexa()

    async def handle_alexa(self):
        await sleep(0.5)
        await self.update_hands()
        if self.get_hand_sum(self.alexa_hand) < 17:
            randomizer = randint(1, 12)
            if randomizer > 9:
                await self.ctx.send("Stand")
            else:
                await self.ctx.send("Hit")
                drawn_card = self.get_card()
                self.alexa_hand.append(drawn_card)
                await self.ctx.send("Drawn Card:" + drawn_card[1] + drawn_card[0])
        elif self.get_hand_sum(self.alexa_hand) >= 17:
            randomizer = randint(1, 20)
            if randomizer > 5:
                await self.ctx.send("Stand")
            else:
                await self.ctx.send("Hit")
                drawn_card = self.get_card()
                self.alexa_hand.append(drawn_card)
                await self.ctx.send("Drawn Card: " + drawn_card[1] + drawn_card[0])
        await self.ctx.send(self.check_hand_valid(self.alexa_hand))
        if self.check_hand_valid(self.alexa_hand) == "Busted...":
            self.win_string = "The player wins! The computer should get smarter..."
            await self.endgame()
        elif self.check_hand_valid(self.alexa_hand) == "Blackjack!":
            self.win_string = "The computer won! Better luck next time..."
            await self.endgame()
        else:
            await self.handle_alexa()

    async def endgame(self):
        await self.update_hands()
        await sleep(0.5)
        await self.ctx.send(self.win_string)


class Games(commands.Cog):
    rps_moves = ["rock", "paper", "scissors"]

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.available_cards = []
        self.player_hand = []
        self.alexa_hand = []

    @commands.group(name="play")
    async def play(self, ctx):
        ...

    @play.command(name="blackjack")
    async def bj(self, ctx):
        foo = BlackJack(ctx)
        await foo.new_game()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        foo = BlackJack(reaction.message.channel, reaction.message)
        await foo.do_player_response(str(reaction) == "🇦")

    @play.command(name="rps")
    async def rps(self, ctx, user_move):
        bot_move = choice(Games.rps_moves)
        if user_move.lower() not in Games.rps_moves:
            await ctx.send("That's an invalid move!")
        else:
            if bot_move == user_move.lower():
                await ctx.send("Tie!")
            else:
                if bot_move == "scissors" and user_move.lower() == "paper":
                    await ctx.send("I threw scissors! Alexa wins!")
                if bot_move == "scissors" and user_move.lower() == "rock":
                    await ctx.send("I threw scissors! " + ctx.author.mention + " wins!")
                if bot_move == "paper" and user_move.lower() == "rock":
                    await ctx.send("I threw paper! Alexa wins!")
                if bot_move == "paper" and user_move.lower() == "scissors":
                    await ctx.send("I threw paper! " + ctx.author.mention + " wins!")
                if bot_move == "rock" and user_move.lower() == "scissors":
                    await ctx.send("I threw rock! Alexa wins!")
                if bot_move == "rock" and user_move.lower() == "paper":
                    await ctx.send("I threw rock! " + ctx.author.mention + " wins!")

    @play.group(name="unfair")
    async def unfair(self, ctx):
        ...

    @unfair.command(name="rps")
    async def unfair_rps(self, ctx, user_move):
        if user_move.lower() not in Games.rps_moves:
            await ctx.send("That's an invalid move!")
        else:
            if user_move == "scissors":
                await ctx.send("I threw rock! Alexa wins!")
            if user_move == "rock":
                await ctx.send("I threw paper! Alexa wins!")
            if user_move == "paper":
                await ctx.send("I threw scissors! Alexa wins!")
