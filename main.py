import pickle
import random as r

import discord
from discord.ext import commands

from item import *

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command('help')

# Credit to Eshaan for assisting with enums as well as the player class and the item list.
"""
Notes for future interactivity update
for cornucopia allow each player to declare intent (whcih item they're going for, whether theyre staying or not, whether they team, etc)

Note- for balance update, ctrl f .set_stat( and adjust as necessary.

Note- for next update try to al,;..................,,,,,,,,,dd in weapons during standard battles.
"""


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='being one buggy mfer'))
    print("Ready")


class stats(enum.Enum):
    STR = 'S'
    CHA = 'C'
    WIS = 'W'
    DEX = 'D'
    CON = 'C'


Names = [
    "Bob1", "Bob2", "Bob3", "Bob4", "Bob5", "Bob6", "Bob7", "Bob8", "Bo1b9",
    "Bob10", "Bob11", "Bob12", "Bob13", "Bob14", "Bob15", "Bob16", "Bob17",
    "Bob18", "Bob19", "Bob20", "Bob21", "Bob22", "Bob23", "Bob24"
]
old_stats = [
    "STR", "DEX", "CON", "WIS", "WIS", "CHA", "STR", "DEX", "CON", "WIS",
    "WIS", "CHA", "STR", "DEX", "CON", "WIS", "WIS", "CHA", "STR", "DEX",
    "CON", "WIS", "WIS", "CHA"
]
s_stats = [
    stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA,
    stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA,
    stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA,
    stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA
]


# await ctx.send(s_stats)
class Player(object):
    def __init__(self, name, constant_of_survival, strong_stat, npc):
        self.is_busy = False
        self.item_list = []
        self.name = name
        self.constant_of_survival = constant_of_survival
        self.strong_stat = strong_stat
        self.npc = npc
        self.is_alive = True
        self.has_crafted = False

    def get_name(self):
        return self.name

    def get_busy(self):
        return self.is_busy

    def set_busy(self, new_busy):
        self.busy = new_busy
        return self.busy

    def __str__(self):
        return (self.name)

    def get_const(self):
        return self.constant_of_survival

    def set_const(self, change):
        # REMEMBER TO PUT SIGN WHEN CALLING
        self.constant_of_survival = self.constant_of_survival + change

    def get_stat(self):
        return self.strong_stat

    def set_stat(self, new_stat):
        self.strong_stat = new_stat
        return self.strong_stat

    def is_npc(self):
        # WORK ON THIS
        return self.npc
        # WORK ON THIS ^^

    def give_item(self, item):
        self.item_list.append(item)
        return item

    def get_items(self):
        return self.item_list

    def get_items_enums(self):
        y = []
        for i in self.item_list:
            y.append(i.value())
        return y

    def set_list(self, item):
        self.item_list = item

    def get_alive(self):
        return self.is_alive

    def set_alive(self, life):
        # life should be a bool
        self.is_alive = life

    def get_crafted(self):
        return self.has_crafted

    def set_crafted(self, crafted):
        self.has_crafted = crafted


# remember to put in teams later
class Team(object):
    pass


# TODO: rewrite this
cornucopia_items = initialize_object_list([
    item_directory.MEDKIT, item_directory.KNIFE, item_directory.SWORD,
    item_directory.RATIONS, item_directory.AXE, item_directory.CORN,
    item_directory.BOW
])
inner_cornucopia_items = initialize_object_list(
    [item_directory.AWP, item_directory.GRENADES, item_directory.KATANA])

all_items = initialize_object_list([
    item_directory.AWP, item_directory.GRENADES, item_directory.KATANA,
    item_directory.MEDKIT, item_directory.KNIFE, item_directory.SWORD,
    item_directory.RATIONS, item_directory.AXE, item_directory.CORN,
    item_directory.BOW
])

sponsor_items = initialize_object_list([
    item_directory.AWP, item_directory.GRENADES, item_directory.KATANA,
    item_directory.MEDKIT, item_directory.KNIFE, item_directory.SWORD,
    item_directory.RATIONS, item_directory.AXE, item_directory.CORN,
    item_directory.BOW, item_directory.MEDKIT, item_directory.KNIFE,
    item_directory.SWORD, item_directory.RATIONS, item_directory.AXE,
    item_directory.CORN, item_directory.BOW
])

craftableItems = initialize_object_list([
    item_directory.WOOD_SPEAR, item_directory.HANDAXE,
    item_directory.STONE_SPEAR, item_directory.BOW
])

num_inner_cornucopia_items = 3
player_options = []
at_corn = []
by_corn = []
dead = []
players = []
is_running = []

docket = []

is_goingToFeast = []


async def game_initialize(ctx):
    for index, i in enumerate(Names):
        player = Player(i, 1, s_stats[index], False)
        # appending player name to players
        players.append(player)
        if not player.get_busy():
            if r.choice([True, False, False, False
                         ]) or player.get_stat() == stats.WIS:
                await ctx.send(
                    f'{player.get_name()} runs away into the arena to avoid the cornucopia.'
                )
                is_running.append(player)
                # Smart Enough to ignore the cornocopia
            else:
                randItem = r.choice(cornucopia_items)
                if r.choice([True, False]):
                    if player.get_stat() == stats.DEX:
                        is_running.append(player)

                        player.give_item(randItem)
                        await ctx.send(
                            f'{player.get_name()} speeds into the cornucopia, randomly grabs {randItem}, and quickly runs away'
                        )
                        # gets an item and runs away
                    else:
                        # forced to fight
                        by_corn.append(player)
                else:
                    at_corn.append(player)
                    # forced to fight in cornucopia


async def died(player: Player, deathReason, ctx):
    players.remove(player)
    dead.append(player)
    await ctx.send(f"{player.get_name()} died from {deathReason}.")


async def fight(player1: Player, player2: Player, ctx):
    # fight function. It just runs based on d20 rolls
    player1.set_busy(True)
    player2.set_busy(True)
    fight_const_x = await gen_fight_const(player1, ctx)
    fight_const_y = await gen_fight_const(player2, ctx)
    if fight_const_x > fight_const_y:
        if player2.get_stat() == stats.CHA:
            player2.set_const(-0.7)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia, but spared {player2.get_name()}'s life. {player2.get_name()} escapes the cornucopia into the arena."
            )
            is_running.append(player2)
        elif player2.get_stat() == stats.CON:
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia, but {player2.get_name()} managed to survive the attack due to their high constitution. {player2.get_name()} escapes the cornucopia into the arena."
            )
            is_running.append(player2)
            player2.set_const(-0.7)
        else:

            dead.append(player2)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia and killed {player2.get_name()} in the fight"
            )
        # player one wins
        return player1
    if fight_const_y > fight_const_x:
        if player1.get_stat() != stats.CHA:
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia, but spared {player1.get_name()}'s life. {player1.get_name()} escapes the cornucopia into the arena."
            )
            is_running.append(player1)
            player1.set_const(-0.7)
        elif player1.get_stat == stats.CON:
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia, but {player1.get_name()} managed to survive the attack due to their high constitution. {player1.get_name()} escapes the cornucopia into the arena."
            )
            is_running.append(player1)
            player1.set_const(-0.7)
        else:
            players.remove(player1)
            dead.append(player1)
            # player 2 wins
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia and killed {player1.get_name()} in the fight"
            )
        return player2
    if fight_const_x == fight_const_y:

        await ctx.send(
            f"{player1.get_name()} fought {player2.get_name()} inside the cornucopia. Both tributes emerged from the battle relatively unscathed."
        )

        if player1.get_stat() == stats.CON:
            player1.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player1.set_const(-0.7)

        if player2.get_stat() == stats.CON:
            player2.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player2.set_const(-0.7)
        # nobody wins
        return None


async def feastFight(player1: Player, player2: Player, ctx):
    # fight function. It just runs based on d20 rolls
    # await ctx.send(player1)

    fight_const_x = await gen_fight_const(player1, ctx)
    fight_const_y = await gen_fight_const(player2, ctx)
    if fight_const_x > fight_const_y:
        if player2.get_stat() == stats.CHA:
            player2.set_const(-0.7)
            if player2.get_const() <= 0:
                is_goingToFeast.remove(player2)
                await died(player2, f"their wounds after fighting {player1}", ctx)

            else:
                await ctx.send(
                    f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia, but spared {player2.get_name()}'s life. {player2.get_name()} escapes the cornucopia into the arena."
                )
                is_goingToFeast.remove(player2)
        elif player2.get_stat() == stats.CON:
            player2.set_const(-0.7)
            if player2.get_const() <= 0:
                return died(player2, f"fighting {player1}", ctx)
            else:
                await ctx.send(
                    f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia, but {player2.get_name()} managed to survive the attack due to their high constitution. {player2.get_name()} escapes the cornucopia into the arena."
                )
                is_goingToFeast.remove(player2)
        else:
            players.remove(player2)
            dead.append(player2)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia and killed {player2.get_name()} in the fight"
            )
            is_goingToFeast.remove(player2)
        # player one wins
        return player1
    if fight_const_y > fight_const_x:
        if player1.get_stat() != stats.CHA:
            player1.set_const(-0.7)
            if player1.get_const() <= 0:
                is_goingToFeast.remove(player1)
                await died(player1, f"their wounds after fighting {player2}", ctx)
            else:
                await ctx.send(
                    f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia, but spared {player1.get_name()}'s life. {player1.get_name()} escapes the cornucopia into the arena."
                )
                is_goingToFeast.remove(player1)
        elif player1.get_stat == stats.CON:
            player1.set_const(-0.7)
            if player1.get_const() <= 0:
                return died(player1, f"fighting {player2}", ctx)
            else:
                await ctx.send(
                    f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia, but {player1.get_name()} managed to survive the attack due to their high constitution. {player1.get_name()} escapes the cornucopia into the arena."
                )
                is_goingToFeast.remove(player1)
        else:
            players.remove(player1)
            dead.append(player1)
            # player 2 wins
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia and killed {player1.get_name()}."
            )
            is_goingToFeast.remove(player1)
        return player2
    if fight_const_x == fight_const_y:

        if player1.get_stat() == stats.CON:
            player1.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player1.set_const(-0.7)

        if player2.get_stat() == stats.CON:
            player2.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player2.set_const(-0.7)

        # NOTE THIS FOLLOWING STATEMENT HAS NOT BEEN TESTED AND COULD JUST KILL ONE WHILE THE OTHER LIVES EVEN WITH THE 0 CONSTANT

        if player1.get_const() <= 0 or player2.get_const() <= 0:
            if player1.get_const() <= 0:
                is_goingToFeast.remove(player1)
                await died(player1, f"their wounds after fighting {player2}", ctx)

            if player2.get_const() <= 0:
                is_goingToFeast.remove(player2)
                await died(player2, f"their wounds after fighting {player1}", ctx)
        else:
            await ctx.send(
                f"{player1.get_name()} fought {player2.get_name()} inside the cornucopia. Both tributes emerged from the battle relatively unscathed. Both remain at the feast."
            )

        # nobody wins
        return None


async def randFight(player1: Player, player2: Player, ctx):
    global docket
    # fight function. It just runs based on d20 rolls
    # await ctx.send(player1)

    fight_const_x = await gen_fight_const(player1)
    fight_const_y = await gen_fight_const(player2)
    if fight_const_x > fight_const_y:
        if player2.get_stat() == stats.CHA:
            player2.set_const(-0.7)
            if player2.get_const() <= 0:
                await died(player2, f"their wounds after fighting {player1}", ctx)

            else:
                await ctx.send(
                    f"{player1.get_name()} won a fight with {player2.get_name()}, but spared {player2.get_name()}'s life. {player2.get_name()} runs away."
                )
        elif player2.get_stat() == stats.CON:
            player2.set_const(-0.7)
            if player2.get_const() <= 0:
                return died(player2, f"fighting {player1}", ctx)
            else:
                await ctx.send(
                    f"{player1.get_name()} won a fight with {player2.get_name()}, but {player2.get_name()} managed to survive the attack due to their high constitution. {player2.get_name()} runs away."
                )
        else:
            players.remove(player2)
            dead.append(player2)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} and killed them in the fight."
            )
        # player one wins
        return player1
    if fight_const_y > fight_const_x:
        if player1.get_stat() != stats.CHA:
            player1.set_const(-0.5)
            if player1.get_const() <= 0:
                await died(player1, f"their wounds after fighting {player2}", ctx)
            else:
                await ctx.send(
                    f"{player2.get_name()} won a fight with {player1.get_name()}, but spared {player1.get_name()}'s life. {player1.get_name()} runs away."
                )
        elif player1.get_stat == stats.CON:
            player1.set_const(-0.5)
            if player1.get_const() <= 0:
                return died(player1, f"their wounds after fighting {player2}", ctx)
            else:
                await ctx.send(
                    f"{player2.get_name()} won a fight with {player1.get_name()}, but {player1.get_name()} managed to survive the attack due to their high constitution. {player1.get_name()} runs away."
                )
        else:
            players.remove(player1)
            dead.append(player1)
            # player 2 wins
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} and killed them."
            )
        return player2
    if fight_const_x == fight_const_y:

        if player1.get_stat() == stats.CON:
            player1.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player1.set_const(-0.7)

        if player2.get_stat() == stats.CON:
            player2.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player2.set_const(-0.7)

        # NOTE THIS FOLLOWING STATEMENT HAS NOT BEEN TESTED AND COULD JUST KILL ONE WHILE THE OTHER LIVES EVEN WITH THE 0 CONSTANT

        if player1.get_const() <= 0 or player2.get_const() <= 0:
            if player1.get_const() <= 0:
                await died(player1, f"their wounds after fighting {player2}", ctx)

            if player2.get_const() <= 0:
                await died(player2, f"their wounds after fighting {player1}", ctx)
        else:
            await ctx.send(
                f"{player1.get_name()} fought {player2.get_name()}. Both tributes emerged from the battle relatively unscathed. Both leave the scene."
            )

        # nobody wins
        return None


# THIS FUNCTIONS IS FOR FIGHTS OVER AN OBJECT
async def item_fight(player1: Player, player2: Player, item, ctx):
    # fight function. It just runs based on d20 rolls
    player1.set_busy(True)
    player2.set_busy(True)
    fight_const_x = await gen_fight_const(player1, ctx)
    fight_const_y = await gen_fight_const(player2, ctx)
    if fight_const_x > fight_const_y:
        if player2.get_stat() == stats.CHA:
            player2.set_const(-0.7)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} over {item}, but spared {player2.get_name()}'s life. {player1.get_name()} Then runs away into the arena."
            )
            is_running.append(player1)
        elif player2.get_stat() == stats.CON:
            player2.set_const(-0.7)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} over {item}, but {player2.get_name()} managed to survive the attack due to their high constitution. {player1.get_name()} Then runs away into the arena."
            )
            is_running.append(player1)
        else:
            players.remove(player2)
            dead.append(player2)
            await ctx.send(
                f"{player1.get_name()} won a fight with {player2.get_name()} over {item} and killed {player2.get_name()} in the fight. {player1.get_name()} Then runs away into the arena."
            )
            is_running.append(player1)
        # player one wins
        player1.give_item(item)
        return player1
    if fight_const_y > fight_const_x:
        if player1.get_stat() != stats.CHA:
            player1.set_const(-0.5)
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} over {item}, but spared {player1.get_name()}'s life. {player2.get_name()} Then runs away into the arena."
            )
            is_running.append(player2)
            is_running.append(player2)
        elif player1.get_stat == stats.CON:
            player1.set_const(-0.5)
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} over {item}, but {player1.get_name()} managed to survive the attack due to their high constitution.{player2.get_name()} Then runs away into the arena."
            )
            is_running.append(player2)
        else:
            players.remove(player1)
            dead.append(player1)
            await ctx.send(
                f"{player2.get_name()} won a fight with {player1.get_name()} over {item} and killed {player1.get_name()} in the fight. {player2.get_name()} Then runs away into the arena."
            )
            is_running.append(player2)
        # player 2 wins
        player2.give_item(item)
        return player2
    if fight_const_x == fight_const_y:

        if r.choice([True, False]):
            player1.give_item(item)
            await ctx.send(
                f"{player1.get_name()} fought {player2.get_name()} over {item} and won it. Both tributes emerged from the battle relatively unscathed. Both tributes then run away into the arena."
            )
        else:
            player2.give_item(item)
            await ctx.send(
                f"{player2.get_name()} fought {player1.get_name()} over {item} and won it. Both tributes emerged from the battle relatively unscathed. Both tributes then run away into the arena."
            )
        is_running.append(player2)
        is_running.append(player1)
        if player1.get_stat() == stats.CON:
            player1.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player1.set_const(-0.7)

        if player2.get_stat() == stats.CON:
            player2.set_const(-0.5)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
        else:
            player2.set_const(-0.7)
        # nobody wins
        return None


async def gen_fight_const(playe: Player, ctx):
    # roll with advantage if str
    if playe.get_stat() == stats.STR:
        return max(r.randint(0, 20), r.randint(0, 20))
    else:
        return r.randint(0, 20)


async def corn_fights(ctx):
    # runs corn functions while someone exists
    while at_corn:
        if len(at_corn) == 1:
            x = at_corn[0]
            # last one standing is the winner
            await ctx.send(
                f"{x.get_name()} is the last remaining tribute at the cornucopia! They gather their loot."
            )
            for i in all_items:
                x.give_item(i)
            at_corn.remove(x)
            is_running.append(x)
            return
        # await ctx.send(len(at_corn))
        p1 = r.choice(at_corn)
        at_corn.remove(p1)
        p2 = r.choice(at_corn)
        at_corn.remove(p2)
        p_winner = await fight(p1, p2, ctx)
        # XD you thought you were fighting? hell naw!

        if p_winner != None:
            at_corn.append(p_winner)
        else:
            at_corn.append(p1)
            at_corn.append(p2)


async def corn_fights2(ctx):
    # runs corn functions while someone exists
    while by_corn:
        if len(by_corn) == 1:
            x = by_corn[0]
            by_corn.remove(x)
            is_running.append(x)
            return
        # await ctx.send(len(by_corn))
        p1 = r.choice(by_corn)
        by_corn.remove(p1)
        p2 = r.choice(by_corn)
        by_corn.remove(p2)
        p_winner = await item_fight(p1, p2, r.choice(cornucopia_items), ctx)
        # XD you thought you were fighting? hell naw!

        if p_winner != None:
            pass


async def sponsorChance(player: Player, activityCoolness, ctx):
    # rolls a D20 at advantege if charisma, and adds coolness mod  to the roll

    x = 0
    if player.get_stat() == stats.CHA:
        x = max(r.randint(0, 20), r.randint(0, 20))
    else:
        x = r.randint(0, 20)

    x += activityCoolness

    if x >= 20:
        # ITEMS REFERENCING EARLIER LIST AND NOT ENUM LIST
        await ctx.send(
            f"{player.get_name()} was sent {r.choice(sponsor_items)} by a mysterious sponsor."
        )
    else:
        pass


async def checkEqual(p1: Player, p2: Player, playerList, isp1, ctx):
    if len(playerList) >= 2 and isp1 == True:
        if p1 not in players:
            np1 = r.choice(playerList)
            return await checkEqual(np1, p2, playerList, True, ctx)
        elif p1 in players:
            return p1
    elif len(playerList) > 2 and isp1 == False:
        if p1 == p2 or p2 not in players:
            np2 = r.choice(playerList)
            return await checkEqual(p1, np2, playerList, False, ctx)
        elif p1 != p2 and p2 in players:
            return p2
    elif len(playerList) == 2 and isp1 == False:
        playerList.remove(p1)
        np2 = playerList[0]
        playerList.append(p1)
        return np2
    else:
        return


async def cuts_tree(player: Player, ctx):
    tool = "e"
    if item_directory.SWORD in player.get_items_enums():
        tool = "sword"
    if item_directory.KATANA in player.get_items_enums():
        tool = "katana"
    if item_directory.AXE in player.get_items_enums():
        tool = "axe"
    await ctx.send(
        f"{player.get_name()} cuts down a tree wth their {tool} and builds a fire with the lumber."
    )

    player.set_const(0.3)

    await sponsorChance(player, 1, ctx)


##############SAVING FOR LATER###################
async def hunts_enemy(p1: Player, p2: Player, ctx):
    # find which weapon triggered the call, and pass it as an argument in randFight Will have to edit prints in randFight.

    # if r.choice([True, False]):
    await ctx.send(f"{p1.get_name()} hunts down {p2.get_name()}.")
    docket.remove(p2)
    winner = randFight(p1, p2, ctx)
    if winner == p1:
        await sponsorChance(p1, 5, ctx)
    elif winner == p2:
        await sponsorChance(p2, 3, ctx)
    else:
        if p1 in players:
            await sponsorChance(p1, 1, ctx)
        if p2 in players:
            await sponsorChance(p2, 1, ctx)
    # else:


##############SAVING FOR LATER###################


async def hunts_food(player: Player, ctx):
    weapon = ""
    p = player.get_items_enums()
    if item_directory.GRENADES in p:
        weapon = "belt of grenades"
    if item_directory.KNIFE in p:
        weapon = "knife"
    if item_directory.SWORD in p:
        weapon = "sword"
    if item_directory.AXE in p:
        weapon = "axe"
    if item_directory.KATANA in p:
        weapon = "katana"
    if item_directory.BOW in p:
        weapon = "bow and arrows"

    # GIVE THE PLAYER A MEAT ITEM IF THEY SUCCEED

    if player.get_stat() == stats.DEX:
        if r.choice([True, True, True, False]):
            await ctx.send(
                f"{player.get_name()} hunts down a deer wth their {weapon} and eats the meat."
            )
            await sponsorChance(player, 3, ctx)

        else:
            await ctx.send(
                f"{player.get_name()} attempts to hunt down a deer wth their {weapon}, however is unable to catch it."
            )
            await sponsorChance(player, 0, ctx)
    else:
        if r.choice([True, False]):
            await ctx.send(
                f"{player.get_name()} hunts down a deer wth their {weapon} and eats the meat."
            )
            if weapon == "belt of grenades":
                """ TENATIVE, NOT YET BEEN TESTED
                player.get_items_enums().remove(item_directory.GRENADES)
                """
                pass
            await sponsorChance(player, 3, ctx)
        else:
            await ctx.send(
                f"{player.get_name()} attempts to hunt down a deer wth their {weapon}, however is unable to catch it."
            )
            await sponsorChance(player, 0, ctx)


async def craft_item(player: Player, ctx):
    # did not give player an item
    item = r.choice(craftableItems)
    await ctx.send(
        f"{player.get_name()} uses their supreme intellect to craft {item.__str__()}"
    )
    player.set_crafted(True)

    await sponsorChance(player, 2, ctx)


async def cactus_juice(player: Player, ctx):
    await ctx.send(
        f"{player.get_name()} finds a cactus and drinks the juice. They then say 'Drink cactus juice! it'll quench ya! nothing's quenchier! It's the quenchiest!'"
    )
    player.set_const(-.1)
    if player.get_const() <= 0:
        await died(player, "drinking cactus juice", ctx)
    else:
        await sponsorChance(player, 3, ctx)


async def snipe(p1: Player, p2: Player, ctx):
    global docket
    weapon = ""
    p = p1.get_items_enums()
    if item_directory.BOW in p:
        weapon = "bow and arrows"
    if item_directory.AWP in p:
        weapon = "AWP"

    if p1.get_stat() == stats.DEX:
        if r.choice([True, True, True, False]):
            await ctx.send(
                f"{p1.get_name()} snipes {p2.get_name()} with their {weapon}."
            )
            if weapon == "AWP":
                for i, item in enumerate(p2.get_items_enums()):
                    p1.give_item(item)
                await died(p2, f"being sniped by {p1.get_name()}", ctx)
                docket.remove(p2)
            else:
                p2.set_const(-0.7)
                if p2.get_const() <= 0:
                    await died(
                        p2,
                        f"their wounds after being sniped by {p1.get_name()}", ctx)
                docket.remove(p2)
            await sponsorChance(p1, 4, ctx)

        else:
            await ctx.send(
                f"{p1.get_name()} attempts to snipe {p2.get_name()} wth their {weapon}, however misses."
            )
            await sponsorChance(p1, 1, ctx)
    else:
        if r.choice([True, False]):
            await ctx.send(
                f"{p1.get_name()} snipes {p2.get_name()} with their {weapon}."
            )
            if weapon == "AWP":
                for i, item in enumerate(p2.get_items_enums()):
                    p1.give_item(item)
                await died(p2, f"being sniped by {p1.get_name()}", ctx)
                docket.remove(p2)
            else:
                p2.set_const(-0.7)
                if p2.get_const() <= 0:
                    await died(
                        p2,
                        f"their wounds after being sniped by {p1.get_name()}", ctx)
                docket.remove(p2)
            await sponsorChance(p1, 4, ctx)
        else:
            await ctx.send(
                f"{p1.get_name()} attempts to snipe {p2.get_name()} wth their {weapon}, however misses."
            )
            await sponsorChance(p1, 1, ctx)


async def grenade_trap(p1: Player, p2: Player, ctx):
    num = r.randint(1, 20)
    await ctx.send(f"{p1.get_name()} sets a trap with their grenade belt.")
    if num > 17:
        await ctx.send(
            f"{p2.get_name()} walked directly into {p1.get_name()}'s trap.")
        docket.remove(p2)
        await died(p2, "blowing up", ctx)
        for i, item in enumerate(p2.get_items()):

            # half of p2's items were destroyed

            if i % 2 == 0:
                p1.give_item(item)
        """
        lst = p1.get_items()
        await ctx.send(lst)
        
        lst = lst.remove(item_directory.GRENADES)
        p1.set_list(lst)
        """
        await sponsorChance(p1, 4, ctx)
    if num > 1 and num <= 17:
        await ctx.send(
            f"Nothing happens and {p1.get_name()} packs up their grenade belt and leaves."
        )
    else:
        await ctx.send(f"{p1.get_name()} accidentally triggers their own trap.")
        await died(p1, "their own trap", ctx)


async def water(player: Player, ctx):
    if r.choice([True, False]):
        await ctx.send(
            f"{player.get_name()} searches for a water source and is successful."
        )
        player.set_const(0.3)
        await sponsorChance(player, 2, ctx)
    else:
        await ctx.send(
            f"{player.get_name()} searches for a water source, however is unable to find one."
        )
        await sponsorChance(player, -1, ctx)


async def bear_trap(player: Player, ctx):
    if player.get_stat() == stats.DEX:
        if r.choice([True, True, True, False]):
            await ctx.send(
                f"{player.get_name()} almost falls into a bear trap, however manages to dodge out of the way before falling in"
            )
            await sponsorChance(player, 2, ctx)
        else:
            await ctx.send(
                f"{player.get_name()} falls into a bear trap and is badly injured"
            )
            player.set_const(-0.7)
            if player.get_const() <= 0:
                await died(player, "a bear trap", ctx)
            else:
                await sponsorChance(player, 2, ctx)
    else:
        if r.choice([True, False]):
            await ctx.send(
                f"{player.get_name()} almost falls into a bear trap, however manages to dodge out of the way before falling in"
            )
            await sponsorChance(player, 2, ctx)
        else:
            await ctx.send(
                f"{player.get_name()} falls into a bear trap and is badly injured"
            )
            player.set_const(-0.7)
            if player.get_const() <= 0:
                await died(player, "a bear trap", ctx)
            else:
                await sponsorChance(player, 2, ctx)


async def randomEventManager(ctx):
    global docket
    # for random events, the function will first check what resources the player has and based upon those will create a custom list of possible events for them. then it will r.choice an event from that list and run a different function based on the choice.

    # docket is all remaining players for this round
    docket = []
    for i in players:
        docket.append(i)

    for index, player in enumerate(players):

        # await ctx.send(f"** **\nRunning {player.get_name()} now of")
        # ps = []
        # for i in docket:
        #     ps.append(i.get_name())
        # await ctx.send(f"{ps}\n ** **")

        # player = i
        pItems = player.get_items_enums()
        try:
            docket.remove(player)
        except ValueError:
            pass

        # checks for healing items and uses them by async default.
        # COMMENTED OUT TEMPORARILY, CODE GIVING ERRORS
        # for i in pItems:
        # if item.get_type() == i.types.ASSIST:
        #    player.set_const(i.get_ass())
        #    pItems.remove(i)

        # checks for bladed items
        # for i in pItems:await ctx.send(type(i))
        # for i in player.get_items_enums():await ctx.send(type(i))

        if item_directory.SWORD in pItems or item_directory.AXE in pItems or item_directory.KATANA in pItems:
            # CUTS TREE
            player_options.append("cuts tree")

        # checks for weapons
        if (
                item_directory.SWORD in pItems or item_directory.AXE in pItems or item_directory.KATANA in pItems or item_directory.KNIFE in pItems or item_directory.GRENADES in pItems or item_directory.BOW in pItems):
            # HUNTS FOOD

            player_options.append("hunts food")

        if (
                item_directory.SWORD in pItems or item_directory.AXE in pItems or item_directory.KATANA in pItems or item_directory.KNIFE in pItems or item_directory.GRENADES in pItems or item_directory.BOW in pItems) and (
                len(docket) >= 1):
            # HUNTS ENEMY, TEMPORARILY COMMENTED FOR TESTING
            player_options.append("hunts enemy")

        # checks for wisdom
        if player.get_stat() == stats.WIS and player.get_crafted() is False:
            # craft item
            player_options.append("craft item")

        if player.get_stat() != stats.WIS:
            # DRINK CACTUS JUICE
            player_options.append("cactus juice")

        if (item_directory.AWP in pItems or item_directory.BOW in pItems) and (len(docket) >= 1):
            # snoipe
            player_options.append("snipe")

        if (item_directory.GRENADES in pItems) and (len(docket) >= 1):
            # trap
            player_options.append("grenade trap")

        # universal
        player_options.append("water")
        player_options.append("bear trap")
        # await ctx.send(player_options)
        rActivity = r.choice(player_options)
        # await ctx.send(f"{player}- {rActivity}")

        # HEYO IM SKIPPING THE ONES THAT REFERENCE OTHER PLAYERS COS IDK EXACTLY HOW TO DO THAT. ACTIVITIES LABELED 'DO LATER' OR 'SAVING FOR LATER' INCLUDE A REFERENCE TO ANOTHER CHARACTER

        if rActivity == "cuts tree":
            await cuts_tree(player, ctx)
        elif rActivity == "hunts enemy":
            p2 = 0
            p1 = await checkEqual(player, p2, players, True, ctx)
            p2 = await checkEqual(p1, r.choice(docket), players, False, ctx)
            await hunts_enemy(p1, p2, ctx)
        elif rActivity == "hunts food":
            await hunts_food(player, ctx)
        elif rActivity == "craft item":
            await craft_item(player, ctx)
        elif rActivity == "cactus juice":
            await cactus_juice(player, ctx)
        elif rActivity == "snipe":
            p2 = 0
            p1 = await checkEqual(player, p2, players, True, ctx)
            p2 = await checkEqual(p1, r.choice(docket), players, False, ctx)
            await snipe(p1, p2, ctx)

        elif rActivity == "grenade trap":
            p2 = 0
            p1 = await checkEqual(player, p2, players, True, ctx)
            p2 = await checkEqual(p1, r.choice(docket), players, False, ctx)
            await grenade_trap(p1, p2, ctx)
        elif rActivity == "water":
            await water(player, ctx)
        elif rActivity == "bear trap":
            await bear_trap(player, ctx)

        player_options.clear()


async def cannons(ctx):
    if len(players) <= 10:
        if len(dead) > 1:
            await ctx.send(f"As night falls, the cannon fires {len(dead)} times.")
            await ctx.send(f"The images of the following tributes flash in the sky:")
            for tribute in dead:
                await ctx.send(tribute.get_name() + "")
            dead.clear()
        elif len(dead) == 1:
            await ctx.send(f"As night falls, the cannon fires 1 time.")
            await ctx.send(f"The image of {dead[0].get_name()} flashes in the sky.")
            dead.clear()
        else:
            await ctx.send(f"As night falls, the cannon remains silent.")
        await ctx.send(f"{len(players)} tributes remain.")
    else:
        if len(dead) > 1:
            await ctx.send(f"As night falls, the cannon fires {len(dead)} times.")
            await ctx.send(f"The images of the following tributes flash in the sky:")
            for tribute in dead:
                await ctx.send(tribute.get_name() + "")
            dead.clear()
        elif len(dead) == 1:
            await ctx.send(f"As night falls, the cannon fires 1 time.")
            await ctx.send(f"The image of {dead[0].get_name()} flashes in the sky.")
            dead.clear()
        else:
            await ctx.send(f"As night falls, the cannon remains silent.")
        await ctx.send(f"{len(players)} tributes remain.")


async def corn_feast(ctx):
    remP = len(players)
    await ctx.send(
        f"An announcement is sent out to the remaining tributes: There are {remP} tributes remaining. We invite them all to return to the cornucopia for new items and resources. The remaining tributes are as follows:"
    )
    for i in range(len(players)):
        await ctx.send(f"{players[i]}")

    for index, player in enumerate(players):

        if player.get_stat() == stats.WIS:
            if r.choice([True, False, False]):
                is_goingToFeast.append(player)
        else:
            if r.choice([True, False]):
                is_goingToFeast.append(player)

    await ctx.send("-----------------------")

    # returns which players are going to the feast
    if len(is_goingToFeast) > 1:
        await ctx.send(
            f"Of the remaining {remP} tributes, {len(is_goingToFeast)} show up to the feast:"
        )

        for member in is_goingToFeast:
            await ctx.send(member)
    elif len(is_goingToFeast) == 1:
        await ctx.send(
            f"Of the remaining {remP} tributes, only {is_goingToFeast[0]} shows up to the feast."
        )
    else:
        await ctx.send(
            f"Of the remaining {remP} tributes, none show up to the feast.")

    await ctx.send("-----------------------")
    for member in is_goingToFeast:

        if member.get_stat() == stats.DEX:
            stolenItem = r.choice(all_items)
            await ctx.send(
                f"{member.get_name()} sneaks into the cornucopia and escapes with {stolenItem}"
            )
            member.give_item(stolenItem)
            is_goingToFeast.remove(member)
    while len(is_goingToFeast) >= 2:
        p2 = 0
        p1 = await checkEqual(r.choice(is_goingToFeast), p2, is_goingToFeast, True, ctx)
        p2 = await checkEqual(p1, r.choice(is_goingToFeast), is_goingToFeast, False, ctx)

        if p2 != p1:
            await feastFight(p1, p2, ctx)

    if len(is_goingToFeast) == 1:
        winner = is_goingToFeast[0]
        await ctx.send(
            f"{winner} is the final tribute remaining at the feast. They loot everything, grab a snack, and finally venture back out into the arena."
        )
        winner.set_const(1)
        for index, i in enumerate(cornucopia_items):
            winner.give_item(i)
            is_goingToFeast.clear()


async def win(ctx):
    await ctx.send(
        f"{players[0]} is the last tribute standing! The hunger games have finished!"
    )

    # implement stats later


async def gameManager(ctx):
    global Names
    await ctx.send("enter 24 names.")
    await ctx.send("the next 24 messages (from anyone) will be interpreted as names for tributes.")

    async def check(m):
        return m.content == 'n' or m.content == 'next'

    async def check2(m):
        return

    # for i in range(24):
    #     await ctx.send(f"enter name {i + 1}")
    #     name = await client.wait_for('message',
    #                                  check=lambda m: m.channel == ctx.channel and m.author.id != 851698738871533580)
    #     Names[i] = str(name.content)

    Names = ["Kai", "Adam", "Thal", "Isaac", "Skylar", "Mark Zuckerberg", "Bingus", "Rowan", "Genghis Khan",
             "Chip Chipson", "Alex", "Joe Mama", "Joaquin", "Jesus", "Juan", "Dwayne \"The Rock\" Johnson", "Emma",
             "Vlad", "Ellen Degeneres", "Hugo", "Scented Marker", "Katie", "Rose", "Mark Ruffalo"]

    await game_initialize(ctx)

    await corn_fights2(ctx)

    await corn_fights(ctx)

    await ctx.send("-----------------------")

    await cannons(ctx)

    await ctx.send("-----------------------")

    await ctx.send("say 'next' or 'n' to continue")

    nxt = client.wait_for('message', check=lambda m: (
                                                             m.content == 'n' or m.content == 'next') and m.channel == ctx.channel and m.author.id != 851698738871533580)

    await ctx.send("-----------------------")

    while len(players) > 10:
        await randomEventManager(ctx)

        await ctx.send("-----------------------")

        await cannons(ctx)

        await ctx.send("-----------------------")

        await ctx.send("say 'next' or 'n' to continue")

        nxt = await client.wait_for('message', check=lambda m: (
                                                                       m.content == 'n' or m.content == 'next') and m.channel == ctx.channel and m.author.id != 851698738871533580)

        await ctx.send("-----------------------")

    await corn_feast(ctx)

    await ctx.send("say 'next' or 'n' to continue")

    nxt = await client.wait_for('message', check=lambda m: (
                                                                   m.content == 'n' or m.content == 'next') and m.channel == ctx.channel and m.author.id != 851698738871533580)

    while len(players) > 1:
        await ctx.send("-----------------------")

        await randomEventManager(ctx)

        await ctx.send("-----------------------")

        await cannons(ctx)

        await ctx.send("-----------------------")

        await ctx.send("say 'next' or 'n' to continue")

        nxt = await client.wait_for('message', check=lambda m: (
                                                                       m.content == 'n' or m.content == 'next') and m.channel == ctx.channel and m.author.id != 851698738871533580)

    if len(players) == 1:
        await ctx.send("<><><><><><><><><><><><>")

        await win(ctx)

        await ctx.send("<><><><><><><><><><><><>")


@client.command(aliases=["b"])
async def begin(ctx):
    await gameManager(ctx)


@client.command(aliases=["gpl"])
async def getPlayerList(ctx):
    pl = []
    for i in players:
        pl.append(i.get_name())
    await ctx.send(pl)


# token = "token"
#
# with open("token.p", "wb") as t:
#     pickle.dump(token, t)

with open("token.p", "rb") as t:
    token = pickle.load(t)

client.run(token)

# make a list of all the people staying, then run it through a function that lets them battle it out.

# with every task that deducts survival mod, if it drops below 0 on that task, then that task kills you.
"""random event ideas: 
if they have a weapon- <name> hunts for food with <weapon> and is/isn't successful,
<name> hunts down <another tribute> and succeeds/fails at killing them. (run fight)

if they have a bladed weapon (knife, sword, axe)- <name> cuts down a tree and uses the wood for a fire. (+0.5 survival mod)

if they don't have a weapon, but have wisdom- <name> crafts <homemade weapon> with natural resources they found laying around.

if they have dexterity- <name> manages to yoink <enemy tribute>'s <item>

if they don't have wisdom- <name> cuts open a cactus and drinks the juice. They immediately say "Drink cactus juice. I'll quench ya. nothing's quenchier. it's the quenchiest." and become temporarily delusional. (-0.5 to survival mod) (and yes, you can die from drinking cactus juice.)

if they have AWP- (2/3rds chance with DEX 1/3rd chance without) <name> manages to snipe <enemy tribute> with an AWP. (1/3rd chance with DEX 2/3rds chance without) <name> barely misses <enemy tribute> with an AWP. | If they hit, the target dies unless they have constitution, in which case they are heavily injured. (-0.7 survival mod)

if they have grenade belt- <name> sets a trap with their grenade belt. roll 1d20. On 16-20: and <enemy tribute> exploded. on 2-15: but nobody fell for it. on 1: but they accidentally set it off. (-0.75 survival mod)

misc- <name> searches for a water source and is/isn't successful (if found +0.5 to survival mod),
<name> almost falls/falls into a bear trap (if they fall -0.5 to survival mod),



"""

# add a function for each random event

# add a function to clear busy from everyone and call it between random events

# add a function that generates random events on a person by person basis
"""
IMPORTANT PAY ATTENTION
NEW INFORMATION: use player.get_item_enums and item_directory.OBJECT in order to get specific weapons
ONLY COMPARE BETWEEN THE item_directory enum and get_item_enums!!!!
initalization of lists in item class for brevity.

"""
