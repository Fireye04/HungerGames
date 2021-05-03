import enum

class types(enum.Enum):
    WEAPON = 'weapons'
    ASSIST = 'assist'

class item_directory(enum.Enum):
    #test_item = ['Name', types.WEAPON, 'assist_value']
    MEDKIT = ['a medkit', types.ASSIST, 0.5]
    KNIFE = ['a knife', types.WEAPON, 0]
    SWORD = ['a sword', types.WEAPON, 0]
    RATIONS = ['some rations', types.ASSIST, 0.25]
    AXE = ['an axe', types.WEAPON, 0]
    CORN = ['some corn', types.ASSIST, 0.25]
    BOW = ['a bow and some arrows', types.WEAPON, 0]
    AWP = ['an AWP', types.WEAPON, 0]
    GRENADES = ['some grenades', types.WEAPON, 0]
    KATANA = ['a katana', types.WEAPON, 0]
    WOOD_SPEAR = ['a wooden spear', types.WEAPON, 0]
    STONE_SPEAR = ['a stone spear', types.WEAPON, 0]
    MEAT = ['a chunk of meat', types.ASSIST, 0.25]
    def __str__(self):
        return self.value[0]
def initialize_object_list(e:list):
    items_list = []
    for i in e:
        items_list.append(item(i))
    return items_list
class item(object):
    def __init__(self, data:item_directory):
        self.it = data
        data = data.value
        self.name = data[0]
        self.type = data[1]
        self.ass_val = data[2]
    def get_type(self):
        return self.type
    def __str__(self):
        return self.name
    def get_ass(self):
        return self.ass_val
    def value(self):
        return self.it