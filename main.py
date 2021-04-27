import enum
import random as r

"""
Notes for future interactivity update
for cornucopia allow each player to declare intent (whcih item they're going for, whether theyre staying or not, whether they team, etc)
"""

# note to self, when picking an enemy to fight for the cornucopia do not pick an enemy with a WIS stat. 

class stats(enum.Enum):
    STR = 'S'
    CHA = 'C'
    WIS = 'W'
    DEX = 'D'
    CON = 'C'
Names = ["Bob", "Bobbina", "Bobette", "Bobetta", "Bobe", "Bobbi", "Bobitty", "Bobby", "Bobera", "Boberta", "Bobo", "Bobert", "Bob13", "Bob14", "Bob15", "Bob16", "Bob17", "Bob18", "Bob19", "Bob20", "Bob21", "Bob22", "Bob23", "Bob24"]
old_stats = ["STR", "DEX", "CON", "WIS", "WIS", "CHA","STR", "DEX", "CON", "WIS", "WIS", "CHA", "STR", "DEX", "CON", "WIS", "WIS", "CHA", "STR", "DEX", "CON", "WIS", "WIS", "CHA"]
s_stats = [stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA,stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA, stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA, stats.STR, stats.DEX, stats.CON, stats.WIS, stats.WIS, stats.CHA]
#print(s_stats)
class Player(object):
    def __init__(self, name, constant_of_survival, strong_stat, npc):
        self.is_busy = False
        self.item_list = []
        self.name = name
        self.constant_of_survival = constant_of_survival
        self.strong_stat = strong_stat
        self.npc = npc
        self.is_alive = True
    def get_name(self):
        return self.name
    def get_busy(self):
        return self.is_busy
    def set_busy(self, new_busy):
        self.busy = new_busy
        return self.busy
    def __str__(self):
        return(self.name)
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
      #WORK ON THIS
      return self.npc
      #WORK ON THIS ^^
    def give_item(self, item):
      self.item_list.append(item)
      return item
    def get_alive(self):
        return self.is_alive
    def set_alive (self, life):
        # life should be a bool
        self.is_alive = life
        
# remember to put in teams later
class Team(object):
    pass

cornocopia_items = ['a medkit', 'a knife', "a sword", "a backpack full of rations", "an axe"]
inner_cornucopia_items = ["an AWP", "a belt of grenades"]
num_inner_cornucopia_items = 3
at_corn = []
players = []
is_running = []
def game_initialize():
    for index, i in enumerate(Names):
        player = Player(i, 1, s_stats[index], False)
        if not player.get_busy():
            if r.choice([True, False, False, False]) or player.get_stat() == stats.WIS:
                print('{name} runs away into the arena to avoid the cornucopia.'.format(name=player.get_name()))
                is_running.append(player)
            else:
                randItem = r.choice(cornocopia_items)
                if r.choice([True, False]):
                    if player.get_stat() == stats.DEX:
                        is_running.append(player)
                        player.give_item(randItem)
                        print('{name} speeds into the cornucopia, randomly grabs {item}, and quickly runs away'.format(name=player.get_name(), item=randItem))
                    else:
                        #forced to fight
                        at_corn.append(player)
                else:
                    print('{name} runs into the cornucopia, grabs {item} and stays'.format(name=player.get_name(), item=randItem))
                    at_corn.append(player)
                    player.give_item(randItem)
def fight(player1:Player, player2:Player):
    player1.set_busy(True)
    player2.set_busy(True)
    fight_const_x = gen_fight_const(player1)
    fight_const_y = gen_fight_const(player2)
    if fight_const_x>fight_const_y:
        if player2.get_stat() != stats.CHA:
            if player2.get_stat() == stats.CON:
                player2.set_const(-0.75)
            else:
                players.remove(player2)
        #player one wins
        return player1
    if fight_const_y>fight_const_x:
        if player1.get_stat() != stats.CHA:
            if player1.get_stat == stats.CON:
                player1.set_const(-0.75)
            else:
                players.remove(player1)
        #player 2 wins
        return player2
    if fight_const_x==fight_const_y:
        if player1.get_stat() == stats.CON:
            player1.set_const(-0.25)
        else:
            player1.set_const(-0.5)
        if player2.get_stat() == stats.CON:
            player2.set_const(-0.25)
        else:
            player2.set_const(-0.5)
        #nobody wins
        return None

def gen_fight_const(player:Player):
    if player.get_stat() == stats.STR:
        return max(r.randint(0,20), r.randint(0,20))

def corn_fights():
    while at_corn:
        p1 = r.choice(at_corn)
        at_corn.remove(p1)
        p2 = r.choice(at_corn)
        at_corn.remove(p2)
        p_winner = fight(p1, p2)
        if p_winner != None:
            pass
            
game_initialize()
for p in at_corn:
    print(p)
                    # make a list of all the people staying, then run it through a function that lets them battle it out.
            



# with every task that deducts survival mod, if it drops below 0 on that task, then that task kills you.

"""random event ideas: 
if they have a weapon- <name> hunts for food with <weapon> and is/isn't successful,
<name> hunts down <another tribute> and succeeds/fails at killing them. (run fight)

if they have a bladed weapon (knife, sword, axe)- <name> cuts down a tree and uses the wood for a fire. (+0.25 survival mod)

if they don't have a weapon, but have wisdom- <name> crafts <homemade weapon> with natural resources they found laying around.

if they have dexterity- <name> manages to yoink <enemy tribute>'s <item>

if they don't have wisdom- <name> cuts open a cactus and drinks the juice. They immediately say "Drink cactus juice. I'll quench ya. nothing's quenchier. it's the quenchiest." and become temporarily delusional. (-0.25 to survival mod) (and yes, you can die from drinking cactus juice.)

if they have AWP and dexterity- (2/3rds chance) <name> manages to snipe <enemy tribute> with an AWP. (1/3rd chance) <name> barely misses <enemy tribute> with an AWP. | If they hit, the target dies unless they have constitution, in which case they are heavily injured. (-0.5 survival mod)

if they have grenade belt- <name> sets a trap with their grenade belt. roll 1d20. On 16-20: and <enemy tribute> exploded. on 2-15: but nobody fell for it. on 1: but they accidentally set it off. (-0.75 survival mod)

misc- <name> searches for a water source and is/isn't successful (if found +0.25 to survival mod),
<name> almost falls/falls into a bear trap (if they fall -0.25 to survival mod),



"""


# add a function for each random event

#add a function to clear busy from everyone and call it between random events

# add a function that generates random events on a person by person basis