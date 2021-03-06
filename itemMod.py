#--------------
# Andrew Johnson
# 20 May, 2016
#
# Simple Text-Based Game
#-------------
"""Classes for item creation plus a bunch of spawn-able items"""
import roomMod as RM

class RoomItem:
    objects = {}        # actual items created
    def __init__(self,name,sweep):
        self.itemName = name
        RoomItem.objects[self.itemName] = self
        RM.rooms[sweep].items[name+" "+self.itemType] = self
        # print("Added a {0} {1} to room {2}".format(name,self,sweep))


    def getDesc(self):
        return self.desc

class Sword(RoomItem):
    objects = {}
    def __init__(self,name,sweep):
        self.itemType = "sword"
        self.equipSlot = "arms"
        super().__init__(name,sweep)
        self.desc = "{0} {1}".format(self.itemName,self.itemType)

class Axe(RoomItem):
    objects = {}
    def __init__(self,name,sweep):
        self.itemType = "axe"
        self.equipSlot = "arms"
        super().__init__(name,sweep)
        self.desc = "{0} {1}".format(self.itemName,self.itemType)

class Shield(RoomItem):
    objects = {}
    def __init__(self,name,sweep):
        self.itemType = "shield"
        self.equipSlot = "arms"
        super().__init__(name,sweep)
        self.desc = "{0} {1}".format(self.itemName,self.itemType)

class Helmet(RoomItem):
    objects = {}
    def __init__(self,name,sweep):
        self.itemType = 'helmet'
        self.equipSlot = 'head'
        super().__init__(name,sweep)
        self.desc = "{0} {1}".format(self.itemName,self.itemType)

class Potion:
    #value = 1,2,3 for different amounts of healing
    values = [10,20,30]
    types = ["Potion","Serum","Elixir"]
    def __init__(self,var,swp):
        """var: type of potion. higher var => higher healing amount"""
        self.var = var
        if var == 0:
            self.amount = self.values[0]
            self.itemType = "Potion"
        elif var == 1:
            self.amount = self.values[1]
            self.itemType = "Serum"
        elif var == 2:
            self.amount = self.values[2]
            self.itemType = "Elixir"
        else:
            print(swp,var)
            raise SystemExit('Bad Potion Creation')
        RM.rooms[swp].items[self.itemType.lower()]=self
        self.desc = "Healing {0}\n  Health + {1}".\
            format(self.itemType,self.amount)

    def getDesc(self):
        return self.desc

#----------
# Functions
#----------
def inRare(adj):
    """Return the key associated with the rarity/difficulty of the adjective"""
    if adj in allAdj[1]:
        return 1
    elif adj in allAdj[2]:
        return 2
    elif adj in allAdj[3]:
        return 3
    else:
        return 0


def isItem(obType,iType):
    """Return true if the object obType is of the class designated by iType"""
    if iType == 'sword':
        return isinstance(obType,Sword)
    elif iType == 'axe':
        return isinstance(obType,Axe)
    elif iType == 'shield':
        return isinstance(obType,Shield)
    elif iType == 'helmet':
        return isinstance(obType,Helmet)
    else:
        pass
        # raise SystemError('Bad item type {} in isItem'.format(iType))


def adjPopulate(adjDict,adjFlag):
    """Method for populating the dictionary of adjectives for a specific item"""
# adjectives with enhancements starting with 'a' will go into dictionaries for weapons
# similarly, adjective enhancements leading with 'd' go to shields and 'h' for helmets
# Returns a dictionary corresponding to the key/values that match the flag
    passDict = {}

    for key in adjDict:
        if adjDict[key][0] == adjFlag:
            passDict[key] = adjDict[key]

    return passDict

#-----------
# Adjectives
#-----------
lowRareAdj = {}
medRareAdj = {}
highRareAdj = {}
allAdj = {1:{},2:{},3:{}}
swordAdj = {1:{},2:{},3:{}}
axeAdj = {1:{},2:{},3:{}}
shieldAdj = {1:{},2:{},3:{}}
helmetAdj = {1:{},2:{},3:{}}

def buildAdj():

    lowRareAdj = {
        "trusty":"a1",
        "reliable":"d1",
        "pointy":"a2",
        "durable":"d2",
        "shiny":"d2",
        "crooked":"a1",
        "decent":"a3",
        "adequate":"h1",
        "lucky":"d2a2h2",
        "smart":"h2",
        "unlucky": "a0"
    }

    medRareAdj = {
        "sharp":"a4",
        "sturdy":'d3',
        "protective":"d4a3h2",
        "viscious":"a4d4",
        "perceptive":"h4d2",
        "strong":"d5",
        "dangerous":"a5",
        "intimidating":"h5"
    }

    highRareAdj = {
        "legendary":"a7d5h5",
        "wise":"h7d5",
        "robust":"d7a5",
        "deadly":"a6d5"
    }

    for adj in lowRareAdj:
        allAdj[1][adj] = lowRareAdj[adj]
    for adj in medRareAdj:
        allAdj[2][adj] = medRareAdj[adj]
    for adj in highRareAdj:
        allAdj[3][adj] = highRareAdj[adj]

    for r in range(1,4):
        swordAdj[r] = adjPopulate(allAdj[r],'a')
        axeAdj[r] = adjPopulate(allAdj[r],'a')
        shieldAdj[r] = adjPopulate(allAdj[r],'d')
        helmetAdj[r] = adjPopulate(allAdj[r],'h')
