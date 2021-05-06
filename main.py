import enum
import random as r
from item import *

"""
Notes for future interactivity update
for cornucopia allow each player to declare intent (whcih item they're going for, whether theyre staying or not, whether they team, etc)
"""

class stats(enum.Enum):
    STR = 'S'
    CHA = 'C'
    WIS = 'W'
    DEX = 'D'
    CON = 'C'
Names = ["Bob1", "Bob2", "Bob3", "Bob4", "Bob5", "Bob6", "Bob7", "Bob8", "Bob9", "Bob10", "Bob11", "Bob12", "Bob13", "Bob14", "Bob15", "Bob16", "Bob17", "Bob18", "Bob19", "Bob20", "Bob21", "Bob22", "Bob23", "Bob24"]
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
        self.has_crafted = False
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
    def get_items (self):
        return self.item_list
    def get_items_enums(self):
        y = []
        for i in self.item_list:
            y.append(i.value())
        return y
    def remove_item (self, item):
        self.item_list.remove(item)
    def get_alive(self):
        return self.is_alive
    def set_alive (self, life):
        # life should be a bool
        self.is_alive = life
    def get_crafted (self):
        return self.has_crafted
    def set_crafted (self, crafted):
        self.has_crafted = crafted
        
# remember to put in teams later
class Team(object):
    pass



#TODO: rewrite this
cornucopia_items = initialize_object_list([item_directory.MEDKIT, item_directory.KNIFE, item_directory.SWORD, item_directory.RATIONS, item_directory.AXE, item_directory.CORN, item_directory.BOW])
inner_cornucopia_items = initialize_object_list([item_directory.AWP, item_directory.GRENADES, item_directory.KATANA])
all_items = cornucopia_items + inner_cornucopia_items

craftableItems = initialize_object_list([item_directory.WOOD_SPEAR, item_directory.HANDAXE, item_directory.STONE_SPEAR, item_directory.BOW])

num_inner_cornucopia_items = 3
player_options = []
at_corn = []
by_corn = []
dead = []
players = []
is_running = []
def game_initialize():
    for index, i in enumerate(Names):
        player = Player(i, 1, s_stats[index], False)
        #appending player name to players
        players.append(player)
        if not player.get_busy():
            if r.choice([True, False, False, False]) or player.get_stat() == stats.WIS:
                print(f'{player.get_name()} runs away into the arena to avoid the cornucopia.\n')
                is_running.append(player)
                #Smart Enough to ignore the cornocopia
            else:
                randItem = r.choice(cornucopia_items)
                if r.choice([True, False]):
                    if player.get_stat() == stats.DEX:
                        is_running.append(player)
                        
                        player.give_item(randItem)
                        print(f'{player.get_name()} speeds into the cornucopia, randomly grabs {randItem}, and quickly runs away\n')
                        #gets an item and runs away
                    else:
                        #forced to fight
                        by_corn.append(player)
                else:
                    at_corn.append(player)
                    #forced to fight in cornucopia


def fight(player1:Player, player2:Player):
    #fight function. It just runs based on d20 rolls
    player1.set_busy(True)
    player2.set_busy(True)
    fight_const_x = gen_fight_const(player1)
    fight_const_y = gen_fight_const(player2)
    if fight_const_x>fight_const_y:
        if player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
            print(f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia, but spared {player2.get_name()}'s life. {player2.get_name()} escapes the cornucopia into the arena.\n")
            is_running.append(player2)
        elif player2.get_stat() == stats.CON:
            print(f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia, but {player2.get_name()} managed to survive the attack due to their high constitution. {player2.get_name()} escapes the cornucopia into the arena.\n")
            is_running.append(player2)
            player2.set_const(-0.5)
        else:
            players.remove(player2)
            dead.append(player2)
            print(f"{player1.get_name()} won a fight with {player2.get_name()} inside the cornucopia and killed {player2.get_name()} in the fight\n")
        #player one wins
        return player1
    if fight_const_y>fight_const_x:
        if player1.get_stat() != stats.CHA:
            print(f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia, but spared {player1.get_name()}'s life. {player1.get_name()} escapes the cornucopia into the arena.\n")
            is_running.append(player1)
            player1.set_const(-0.5)
        elif player1.get_stat == stats.CON:
            print(f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia, but {player1.get_name()} managed to survive the attack due to their high constitution. {player1.get_name()} escapes the cornucopia into the arena.\n")
            is_running.append(player1)
            player1.set_const(-0.5)
        else:
            players.remove(player1)
            dead.append(player1)
            #player 2 wins
            print(f"{player2.get_name()} won a fight with {player1.get_name()} inside the cornucopia and killed {player1.get_name()} in the fight\n")
        return player2
    if fight_const_x==fight_const_y:
        
        print(f"{player1.get_name()} fought {player2.get_name()} inside the cornucopia. Both tributes emerged from the battle relatively unscathed.\n")

        if player1.get_stat() == stats.CON:
            player1.set_const(-0.1)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.1)
        else:
            player1.set_const(-0.25)
        
        if player2.get_stat() == stats.CON:
            player2.set_const(-0.1)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.1)
        else:
            player2.set_const(-0.25)
        #nobody wins
        return None

# THIS FUNCTIONS IS FOR FIGHTS OVER AN OBJECT
def item_fight(player1:Player, player2:Player, item):
    #fight function. It just runs based on d20 rolls
    player1.set_busy(True)
    player2.set_busy(True)
    fight_const_x = gen_fight_const(player1)
    fight_const_y = gen_fight_const(player2)
    if fight_const_x>fight_const_y:
        if player2.get_stat() == stats.CHA:
            player2.set_const(-0.5)
            print(f"{player1.get_name()} won a fight with {player2.get_name()} over {item}, but spared {player2.get_name()}'s life. {player1.get_name()} Then runs away into the arena.\n")
            is_running.append(player1)
        elif player2.get_stat() == stats.CON:
            player2.set_const(-0.25)
            print(f"{player1.get_name()} won a fight with {player2.get_name()} over {item}, but {player2.get_name()} managed to survive the attack due to their high constitution. {player1.get_name()} Then runs away into the arena.\n")
            is_running.append(player1)
        else:
            players.remove(player2)
            dead.append(player2)
            print(f"{player1.get_name()} won a fight with {player2.get_name()} over {item} and killed {player2.get_name()} in the fight. {player1.get_name()} Then runs away into the arena.\n")
            is_running.append(player1)
        #player one wins
        player1.give_item(item)
        return player1
    if fight_const_y>fight_const_x:
        if player1.get_stat() != stats.CHA:
            player1.set_const(-0.5)
            print(f"{player2.get_name()} won a fight with {player1.get_name()} over {item}, but spared {player1.get_name()}'s life. {player2.get_name()} Then runs away into the arena.\n")
            is_running.append(player2)
            is_running.append(player2)
        elif player1.get_stat == stats.CON:
            player1.set_const(-0.25)
            print(f"{player2.get_name()} won a fight with {player1.get_name()} over {item}, but {player1.get_name()} managed to survive the attack due to their high constitution.{player2.get_name()} Then runs away into the arena.\n")
            is_running.append(player2)
        else:
            players.remove(player1)
            dead.append(player1)
            print(f"{player2.get_name()} won a fight with {player1.get_name()} over {item} and killed {player1.get_name()} in the fight. {player2.get_name()} Then runs away into the arena.\n")
            is_running.append(player2)
        #player 2 wins
        player2.give_item(item)
        return player2
    if fight_const_x==fight_const_y:

        if r.choice([True, False]):
            player1.give_item(item)
            print(f"{player1.get_name()} fought {player2.get_name()} over {item} and won it. Both tributes emerged from the battle relatively unscathed. Both tributes then run away into the arena.\n")
        else:
            player2.give_item(item)
            print(f"{player2.get_name()} fought {player1.get_name()} over {item} and won it. Both tributes emerged from the battle relatively unscathed. Both tributes then run away into the arena.\n")
        is_running.append(player2)
        is_running.append(player1)
        if player1.get_stat() == stats.CON:
            player1.set_const(-0.1)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.1)
        else:
            player1.set_const(-0.25)
        
        if player2.get_stat() == stats.CON:
            player2.set_const(-0.1)
        elif player2.get_stat() == stats.CHA:
            player2.set_const(-0.1)
        else:
            player2.set_const(-0.25)
        #nobody wins
        return None


def gen_fight_const(player:Player):
    #roll with advantage if str
    if player.get_stat() == stats.STR:
        return max(r.randint(0,20), r.randint(0,20))
    else:
        return r.randint(0,20)

def corn_fights():
    #runs corn functions while someone exists
    while at_corn:
        if(len(at_corn) == 1):
            x = at_corn[0]
            #last one standing is the winner
            print(f"{x.get_name()} is the last remaining tribute at the cornucopia! They gather their loot.\n")
            for i in all_items:
                x.give_item(i)
            at_corn.remove(x)
            is_running.append(x)
            return
        #print(len(at_corn))
        p1 = r.choice(at_corn)
        at_corn.remove(p1)
        p2 = r.choice(at_corn)
        at_corn.remove(p2)
        p_winner = fight(p1, p2)
        # XD you thought you were fighting? hell naw!
        
        if p_winner != None:
            at_corn.append(p_winner)
        else:
            at_corn.append(p1)
            at_corn.append(p2)

def corn_fights2():
    #runs corn functions while someone exists
    while by_corn:
        if(len(by_corn) == 1):
            x = by_corn[0]
            by_corn.remove(x)
            is_running.append(x)
            return
        #print(len(by_corn))
        p1 = r.choice(by_corn)
        by_corn.remove(p1)
        p2 = r.choice(by_corn)
        by_corn.remove(p2)
        p_winner = item_fight(p1, p2, r.choice(cornucopia_items))
        # XD you thought you were fighting? hell naw!
        
        if p_winner != None:
            pass

def sponsorChance (player:Player, activityCoolness):
    #rolls a D20 at advantege if charisma, and adds coolness mod  to the roll

    x = 0
    if player.get_stat() == stats.CHA:
        x = max(r.randint(0,20), r.randint(0,20))
    else:
        x = r.randint(0,20)

    x += activityCoolness

    if x >= 19:
        # ITEMS REFERENCING EARLIER LIST AND NOT ENUM LIST
        print(f"{player.get_name()} was sent {r.choice(all_items)} by a mysterious sponsor.\n")


def cuts_tree (player:Player):
    tool = "e"
    if item_directory.SWORD in player.get_items_enums():
        tool = "sword"
    if item_directory.KATANA in player.get_items_enums():
        tool = "katana"
    if item_directory.AXE in player.get_items_enums():
        tool = "axe"
    print(f"{player.get_name()} cuts down a tree wth their {tool} and builds a fire with the lumber.\n")

    player.set_const(0.25)

    sponsorChance(player, 1)

##############SAVING FOR LATER###################
def hunts_enemy (player:Player):
    
    print(f"{player.get_name()} hunts down an enemy.\n")

    sponsorChance(player, 5)
##############SAVING FOR LATER###################

def hunts_food (player:Player):
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
            print(f"{player.get_name()} hunts down a deer wth their {weapon} and eats the meat.\n")
            sponsorChance(player, 3)

        else:
            print(f"{player.get_name()} attempts to hunt down a deer wth their {weapon}, however is unable to catch it.\n")
            sponsorChance(player, 0)
    else:
        if r.choice([True, False]):
            print(f"{player.get_name()} hunts down a deer wth their {weapon} and eats the meat.\n")
            if weapon == "belt of grenades":
                """ TENATIVE, NOT YET BEEN TESTED
                player.get_items_enums().remove(item_directory.GRENADES)
                """
                pass
            sponsorChance(player, 3)
        else:
            print(f"{player.get_name()} attempts to hunt down a deer wth their {weapon}, however is unable to catch it.\n")
            sponsorChance(player, 0)

def craft_item (player:Player):
    item = r.choice(craftableItems)
    print(f"{player.get_name()} uses their supreme intellect to craft {item.__str__()}\n")
    player.set_crafted(True)

    sponsorChance(player, 2)
    
def cactus_juice  (player:Player):
    print(f"{player.get_name()} finds a cactus and drinks the juice. They then say 'Drink cactus juice! it'll quench ya! nothing's quenchier! It's the quenchiest!', and become delusional for about 30 minutes\n")
    player.set_const(-.25)

    sponsorChance(player, 3)
    
##############SAVING FOR LATER###################
"""
def snipe (player):
    p = player.get_items_enums()
    if item_directory.BOW in p:
        weapon = "bow and arrows"
    if item_directory.AWP in p:
        weapon = "AWP"


    if player.get_stat() == stats.DEX:
        if r.choice([True, True, True, False]):
            print(f"{player.get_name()} hunts down a deer wth their {weapon} and eats the meat.\n")
            sponsorChance(player, 4)

        else:
            print(f"{player.get_name()} attempts to hunt down a deer wth their {weapon}, however is unable to catch it.\n")
            sponsorChance(player, 1)
    else:
        if r.choice([True, False]):
            print(f"{player.get_name()} hunts down a deer wth their {weapon} and eats the meat.\n")
            if weapon == "belt of grenades":
                 #TENATIVE, NOT YET BEEN TESTED
                #player.get_items_enums().remove(item_directory.GRENADES)
                pass
            sponsorChance(player, 4)
        else:
            print(f"{player.get_name()} attempts to hunt down a deer wth their {weapon}, however is unable to catch it.\n")
            sponsorChance(player, 1)




def grenade_trap (player:Player):
    print(f"")
"""
##############SAVING FOR LATER###################

def water (player:Player):

    if r.choice([True, False]):
        print(f"{player.get_name()} searches for a water source and is successful.\n")
        player.set_const(0.5)
        sponsorChance(player, 2)
    else:
        print(f"{player.get_name()} searches for a water source, however is unable to find one.\n")
        sponsorChance(player, -1)

def bear_trap(player:Player):
    if player.get_stat() == stats.DEX:
        if r.choice([True, True, True, False]):
            print(f"{player.get_name()} almost falls into a bear trap, however manages to dodge out of the way before falling in\n")
            sponsorChance(player, 2)
        else:
            print(f"{player.get_name()} falls into a bear trap and is badly injured\n")
            player.set_const(-0.5)
            sponsorChance(player, 2)
    else:
        if r.choice([True, False]):
            print(f"{player.get_name()} almost falls into a bear trap, however manages to dodge out of the way before falling in\n")
            sponsorChance(player, 2)
        else:
            print(f"{player.get_name()} falls into a bear trap and is badly injured\n")
            player.set_const(-0.5)
            sponsorChance(player, 2)        

def randomEventManager ():
    # for random events, the function will first check what resources the player has and based upon those will create a custom list of possible events for them. then it will r.choice an event from that list and run a different function based on the choice.

    for index, player in enumerate(players):
        #player = i
        pItems = player.get_items_enums()

        #checks for healing items and uses them by default.
        """ COMMENTED OUT TEMPORARILY, CODE GIVING ERRORS
        for i in pItems:
            if i.get_type() == types.ASSIST:
                player.set_const(i.get_ass())
                pItems.remove(i)
        """

        #checks for bladed items
        #for i in pItems:print(type(i))
        #for i in player.get_items_enums():print(type(i))
        
        if item_directory.SWORD in pItems or item_directory.AXE in pItems or item_directory.KATANA in pItems:
            #CUTS TREE
            player_options.append("cuts tree")

        #checks for weapons
        if item_directory.SWORD in pItems or item_directory.AXE in pItems or item_directory.KATANA in pItems  or item_directory.KNIFE in pItems or item_directory.GRENADES in pItems or item_directory.BOW in pItems:
            #HUNTS ENEMY, TEMPORARILY COMMENTED FOR TESTING
            #player_options.append("hunts enemy")
            #HUNTS FOOD
            player_options.append("hunts food")
        
        #checks for wisdom
        if player.get_stat() == stats.WIS and player.get_crafted() == False:
            #craft item
            player_options.append("craft item")

        if player.get_stat() != stats.WIS:
            #DRINK CACTUS JUICE
            player_options.append("cactus juice")

        if item_directory.AWP in pItems or item_directory.BOW in pItems:
            #snoipe
            player_options.append("snipe")

        if item_directory.GRENADES in pItems:
            #trap
            player_options.append("grenade trap")

        #universal
        player_options.append("water")
        player_options.append("bear trap")
        #print(player_options)
        rActivity = r.choice(player_options)
        print(f"{player}- {rActivity}")
        
        # HEYO IM SKIPPING THE ONES THAT REFERENCE OTHER PLAYERS COS IDK EXACTLY HOW TO DO THAT. ACTIVITIES LABELED 'DO LATER' OR 'SAVING FOR LATER' INCLUDE A REFERENCE TO ANOTHER CHARACTER
        if rActivity == "cuts tree":
            cuts_tree(player)
        elif rActivity == "hunts enemy":
            # DO LATER
            pass
        elif rActivity == "hunts food":
            hunts_food(player)
        elif rActivity == "craft item":
            craft_item(player)
        elif rActivity == "cactus juice":
            cactus_juice(player)
        elif rActivity == "snipe":
            #DO LATER
            pass
        elif rActivity == "grenade trap":
            #DO LATER
            pass
        elif rActivity == "water":
            water(player)
        elif rActivity == "bear trap":
            bear_trap(player)
        
        player_options.clear()
        
        


def cannons ():
    if len(dead) > 0:
        print(f"As night falls, the cannon fires {len(dead)} times.\n")
        print(f"The images of the following tributes flash in the sky:\n")
        for tribute in dead:   
            print(tribute.get_name() + "\n")
        dead.clear()
    elif len(dead) == 1:
        print(f"As night falls, the cannon fires 1 time.\n")
        print(f"The image of {tribute.get_name()} flashes in the sky.\n")
        dead.clear()
    else:
        print(f"As night falls, the cannon remains silent.\n")


def gameManager ():
    game_initialize()

    corn_fights2()

    corn_fights()

    cannons()

    randomEventManager()


gameManager()




# make a list of all the people staying, then run it through a function that lets them battle it out.
            



# with every task that deducts survival mod, if it drops below 0 on that task, then that task kills you.

"""random event ideas: 
if they have a weapon- <name> hunts for food with <weapon> and is/isn't successful,
<name> hunts down <another tribute> and succeeds/fails at killing them. (run fight)

if they have a bladed weapon (knife, sword, axe)- <name> cuts down a tree and uses the wood for a fire. (+0.25 survival mod)

if they don't have a weapon, but have wisdom- <name> crafts <homemade weapon> with natural resources they found laying around.

if they have dexterity- <name> manages to yoink <enemy tribute>'s <item>

if they don't have wisdom- <name> cuts open a cactus and drinks the juice. They immediately say "Drink cactus juice. I'll quench ya. nothing's quenchier. it's the quenchiest." and become temporarily delusional. (-0.25 to survival mod) (and yes, you can die from drinking cactus juice.)

if they have AWP- (2/3rds chance with DEX 1/3rd chance without) <name> manages to snipe <enemy tribute> with an AWP. (1/3rd chance with DEX 2/3rds chance without) <name> barely misses <enemy tribute> with an AWP. | If they hit, the target dies unless they have constitution, in which case they are heavily injured. (-0.5 survival mod)

if they have grenade belt- <name> sets a trap with their grenade belt. roll 1d20. On 16-20: and <enemy tribute> exploded. on 2-15: but nobody fell for it. on 1: but they accidentally set it off. (-0.75 survival mod)

misc- <name> searches for a water source and is/isn't successful (if found +0.25 to survival mod),
<name> almost falls/falls into a bear trap (if they fall -0.25 to survival mod),



"""


# add a function for each random event

#add a function to clear busy from everyone and call it between random events

# add a function that generates random events on a person by person basis

"""
IMPORTANT PAY ATTENTION
NEW INFORMATION: use player.get_item_enums and item_directory.OBJECT in order to get specific weapons
ONLY COMPARE BETWEEN THE item_directory enum and get_item_enums!!!!
initalization of lists in item class for brevity.

"""