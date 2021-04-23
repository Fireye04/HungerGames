import enum
import random as r

"""
Notes for future interactivity update
for cornucopia allow each player to declare intent (whcih item they're going for, whether theyre staying or not, whether they team, etc)
"""


class stats(enum.Enum):
    STR = ''
    CHA = ''
    WIS = ''
    INT = ''
    DEX = ''
    CON = ''
Names = ["Bob1", "Bob2", "Bob3", "Bob4", "Bob5", "Bob6", "Bob7", "Bob8", "Bob9", "Bob10", "Bob11", "Bob12", "Bob13", "Bob14", "Bob15", "Bob16", "Bob17", "Bob18", "Bob19", "Bob20", "Bob21", "Bob22", "Bob23", "Bob24"]
s_stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA","STR", "DEX", "CON", "INT", "WIS", "CHA", "STR", "DEX", "CON", "INT", "WIS", "CHA", "STR", "DEX", "CON", "INT", "WIS", "CHA"]
class Player(object):
    def __init__(self, name, constant_of_survival, strong_stat, npc):
        self.is_busy = False
        self.item_list = []
        self.name = name
        self.constant_of_survival = constant_of_survival
        self.strong_stat = strong_stat
        self.npc = npc
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
        self.constant_of_survival = self.constant_of_survival + 1
    def get_stat(self):
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
    for i in range(len(Names)):
        playerX = Player(Names[i], 1, s_stats[i], False)
        players.append(playerX)
        if r.choice([True, False]):
            #FIRST STAY OR Run
            print(f"{Names[i]} runs away into the arena.")
            is_running.append(playerX)
        else:
            randItem = r.choice(cornocopia_items)
            if r.choice([True, False]):
                #Second stay or run
                if playerX.get_stat() == 'DEX':
                    # if good stat is dex, they get out with an item scot free
                    is_running.append(playerX)
                    print(f"{Names[i]} runs into the cornucpoia, randomly grabs {randItem}, and runs into the arena.")
                else:
                    # fights over item in cornucopia. 
                    print(f"{Names[i]} runs into the cornucpoia and grabs {randItem}.")
                    at_corn.append(playerX)
                playerX.give_item(randItem)
            else:
                # In cornucopia and staying
                print(f'{Names[i]} runs into the cornucopia, grabs {randItem} and stays')
                playerX.give_item(randItem)
            
start_game()
