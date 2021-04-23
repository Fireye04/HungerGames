import enum
import random as r

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
        
# remember to put in teams later
class Team(object):
    pass

cornocopia_items = ['Food', 'Water']
at_corn = []
players = []
is_running = []
def start_game():
    #print(s_stats)
    for i in range(len(Names)):
        playerX = Player(Names[i], 1, s_stats[i], False)
        if playerX.get_busy() == False:
            players.append(playerX)
            # smart players will run away by default to avoid a frontal fight
            if r.choice([True, False, False, False]) or playerX.get_stat() == stats.WIS:
                #print(playerX.get_stat())
                #FIRST STAY OR Run
                print(f"{playerX.get_name()} runs away into the arena to avoid the cornucopia.")
                is_running.append(playerX)
            else:
                #print(playerX.get_stat())
                randItem = r.choice(cornocopia_items)
                #set to true for testing change back
                if True:
                    #Second stay or run
                    if i != 23:
                        if playerX.get_stat() == stats.DEX:
                            # if good stat is dex, they get out with an item scot free
                            is_running.append(playerX)
                            print(f"{playerX.get_name()} speeds into the cornucpoia, randomly grabs {randItem}, and quickly runs away into the arena.")
                            playerX.give_item(randItem)
                        else:
                            # fights over item in cornucopia. 
                            #only use this iteration on the first fight, as it DOES NOT account for deaths
                            playerXplusone = Player(Names[i+1], 1, s_stats[i+1], False)
                            playerXplusone.set_busy(True)
                            # Running fights off d20 rolls. 1-15 will win in a melee battle if they have str and the other doesn't. 1-10 if they're equally matched. If they lose and have a charisma stat, they get a 1d2 roll to be spared. if they have a con stat they have a chance of surving the attack.
                            fight = r.randint(1,20)
                            #if playerX has STR and Xplusone doesn't
                            if playerX.get_stat() == stats.STR and playerXplusone.get_stat() != stats.STR:
                                if fight >= 2 and fight <= 15:
                                    if playerXplusone.get_stat() == stats.CON:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} survives due to his high constitution.")
                                        playerX.give_item(randItem)
                                        playerXplusone.set_const(-0.25)
                                    elif playerXplusone.get_stat() == stats.CHA:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} takes mercy on {playerXplusone.get_name()}, and spares his life.")
                                        playerX.give_item(randItem)
                                        playerXplusone.set_const(-0.25)
                                elif fight == 1:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} was killed in the fight.")
                                    #SET PLAYERXPLUSONE TO DEAD
                                    playerX.give_item(randItem)
                                elif fight == 20:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} was heavily injured in the fight.")
                                    playerXplusone.give_item(randItem)
                                    playerX.set_const(-0.5)
                                    playerXplusone.set_const(-0.25)
                                else:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. Both tributes emerge relatively unscathed.")
                                    playerXplusone.give_item(randItem)
                            #if playerX doesn't have STR and Xplusone does
                            elif playerXplusone.get_stat() == stats.STR and playerX.get_stat() != stats.STR:
                                if fight >= 2 and fight <= 15:
                                    if playerX.get_stat() == stats.CON:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} survives due to his high constitution.")
                                        playerXplusone.give_item(randItem)
                                        playerX.set_const(-0.25)
                                    elif playerX.get_stat() == stats.CHA:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} takes mercy on {playerX.get_name()}, and spares his life.")
                                        playerXplusone.give_item(randItem)
                                        playerX.set_const(-0.25)
                                elif fight == 1:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} was killed in the fight.")
                                    #SET PLAYERX TO DEAD
                                    playerXplusone.give_item(randItem)
                                elif fight == 20:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} was heavily injured in the fight.")
                                    playerX.give_item(randItem)
                                    playerXplusone.set_const(-0.5)
                                else:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. Both tributes emerge relatively unscathed.")
                                    playerX.give_item(randItem)
                            #if both have STR
                            elif playerXplusone.get_stat() == stats.STR and playerX.get_stat() == stats.STR:
                                if fight >= 2 and fight <= 10:
                                    if playerXplusone.get_stat() == stats.CON:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} survives due to his high constitution.")
                                        playerX.give_item(randItem)
                                        playerXplusone.set_const(-0.25)
                                    elif playerXplusone.get_stat() == stats.CHA:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} takes mercy on {playerXplusone.get_name()}, and spares his life.")
                                        playerX.give_item(randItem)
                                        playerXplusone.set_const(-0.25)
                                elif fight == 1:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} was killed in the fight.")
                                    #SET PLAYERXPLUSONE TO DEAD
                                    playerX.give_item(randItem)
                                elif fight == 20:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} was killed in the fight.")
                                    #SET PLAYERX TO DEAD
                                    playerXplusone.give_item(randItem)
                                else:
                                    if playerX.get_stat() == stats.CON:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} survives due to his high constitution.")
                                        playerXplusone.give_item(randItem)
                                        playerX.set_const(-0.25)
                                    elif playerX.get_stat() == stats.CHA:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} takes mercy on {playerX.get_name()}, and spares his life.")
                                        playerXplusone.give_item(randItem)
                                        playerX.set_const(-0.25)
                            #if neither have STR
                            else:
                                if fight >= 2 and fight <= 10:
                                    if playerXplusone.get_stat() == stats.CON:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} survives due to his high constitution.")
                                        playerX.give_item(randItem)
                                        playerXplusone.set_const(-0.25)
                                    elif playerXplusone.get_stat() == stats.CHA:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} takes mercy on {playerXplusone.get_name()}, and spares his life.")
                                        playerX.give_item(randItem)
                                        playerXplusone.set_const(-0.25)
                                elif fight == 1:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and wins a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} was heavily injured in the fight.")
                                    playerX.give_item(randItem)
                                    playerXplusone.set_const(-0.5)
                                elif fight == 20:
                                    print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} was heavily injured in the fight.")
                                    playerXplusone.give_item(randItem)
                                    playerX.set_const(-0.5)
                                else:
                                    if playerX.get_stat() == stats.CON:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerX.get_name()} survives due to his high constitution.")
                                        playerXplusone.give_item(randItem)
                                        playerX.set_const(-0.25)
                                    elif playerX.get_stat() == stats.CHA:
                                        print(f"{playerX.get_name()} runs towards the cornucpoia and loses a fight with {playerXplusone.get_name()} over {randItem}. {playerXplusone.get_name()} takes mercy on {playerX.get_name()}, and spares his life.")
                                        playerXplusone.give_item(randItem)
                                        playerX.set_const(-0.25)
                            
                        
                    else:
                        is_running.append(playerX)
                        print(f"{playerX.get_name()} goes into the cornucpoia, randomly grabs {randItem}, and quickly runs away into the arena.")
                else:
                    # In cornucopia and staying
                    print(f'{playerX.get_name()} runs into the cornucopia, grabs {randItem} and stays')
                    at_corn.append(playerX)
                    playerX.give_item(randItem)
            
start_game()
