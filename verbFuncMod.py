#-------------
# Andrew Johnson
#
# Simple Text based Game
#-------------

"""Module for various verb functions"""
#----------------------
#	Modules Import
#----------------------
import classMod as CM
import itemMod as IM
import roomMod as RM
#----------------------
#	Verb Functions
#----------------------

def say(noun = None):
	"""Say something"""
	if (noun != None):
		return 'You said "{}"'.format(noun)
	else:
		return 'You said nothing.'


def examine(noun = None):
	"""Examine items, enemies, yourself, or the room"""
	if (noun != None):
		swp = CM.getLoc()
		if (noun in RM.rooms[swp].items or noun in RM.rooms[swp].enemies) and \
			noun in CM.GameCharacter.objects:
			return CM.GameCharacter.objects[noun].getDesc()
		elif noun.lower() == 'room':
			return examineRoom()
		else:
			return "There is no {} here".format(noun)
	else:
		return "Need target to examine."


def examineRoom():
	"""Displays the items and enemies in the player's room"""
	thisSwp = CM.getLoc()
	thisRoom = RM.sweepFunc(thisSwp)
	roomStr = "Current room: ({0},{1})\n".format(thisRoom[0],thisRoom[1])
	if len(RM.rooms[thisSwp].enemies) > 0:
		roomStr += 'Enemies: \n'
		for thing in list(RM.rooms[thisSwp].enemies):
			thingType = CM.GameCharacter.objects[thing].className
			if isinstance(RM.rooms[thisSwp].enemies[thing],CM.Player) != True:
				# thingType = CM.GameCharacter.objects[thing].className
				roomStr += '  '+thing.capitalize()#+' the '+thingType+'\n'
			else:
				roomStr += '  '+pName.capitalize()#+' the '+thingType+'\n'
			roomStr +=' the '+thingType+'\n'
	else:
		roomStr += 'Enemies: None\n'
	if len(RM.rooms[thisSwp].items) > 0:
		roomStr += 'Items: \n'
		for item in list(RM.rooms[thisSwp].items):
			iType = RM.rooms[thisSwp].items[item]
			if isinstance(iType,IM.Potion):
				roomStr += "  "+iType.itemType+"\n"
			else:
				roomStr += '  '+item+' '+iType.itemType+'\n'
	else:
		roomStr += 'Items: None'
	return roomStr.strip()


def drink(noun = None):
	"""Drink a healing potion from your inventory"""
	if noun == None:
		#-------CALL A FUNCTION TO SHOW ALL POTIONS
		return "Need a target to drink"
	# else:
	# 	if CM.Player.values[0] == CM.Player.maxHealth:
	# 		return "Already at full health. No need to heal"
	# if noun == "potion":
	# 	typ = 0
	# elif noun == "serum":
	# 	typ  = 1
	# elif noun == "elixir":
	# 	typ = 2
	# 	else:
	# 		return "you have no {} to drink".format(noun)
	# 	if CM.Player.potion[typ] > 0:
	# 		CM.Player.potion[typ] -= 1
	# 		if CM.Player.values[0] + IM.Potions.amounts[typ] >= CM.Player.maxHealth:
	# 			CM.Player.values[0] = CM.Player.maxHealth
	# 		else:
	# 			CM.Player.values[0] += IM.Potions.amounts[typ]
	# 		return "You drank the {0}. Current health: {1}/{2:<}".\
	# 			format(IM.Potion.types[typ],CM.Player.values[0],CM.Player.maxHealth)
	else:
		if noun == "potion":
			typ = 0
		elif noun == "serum":
			typ  = 1
		elif noun == "elixir":
			typ = 2
		rString =  CM.Player.drink(typ)
		if rString == 0:
			return "You have no {} to drink".format(noun)
		else:
			return rString

def hit(noun = None):
	"""Hit an enemy"""
	if (noun != None):
		if noun in CM.GameCharacter.objects:
# there is a noun to hit
			thing = CM.GameCharacter.objects[noun]
# thing is the class of noun
			combatDiff = CM.GameCharacter.objects['you'].values[1] -\
				thing.values[2]
			# difference between player attack and enemy defense
			if combatDiff > 0:
				thing.values[0] -= combatDiff
				if thing.values[0] <= 0:
					return "You killed {}!".format(thing.name.capitalize())
				else:
					return "You hit {0}. Current health: {1}".\
						format(thing.name.capitalize(),thing.values[0])
			else:
				return "{} to strong. Attack not effective".\
					format(thing.name.capitalize())
		else:
			return "There is no {} here.".format(noun)
	else:
		return 'Need target to hit'


def take(takeItem = None):
	"""Pick up item and add to inventory"""
	if(takeItem != None):
		pLoc = CM.getLoc()
		if takeItem in RM.rooms[pLoc].items:
			thing = RM.rooms[pLoc].items[takeItem]
			del RM.rooms[pLoc].items[takeItem]
			if isinstance(thing,IM.Potion):
				CM.Player.potions[thing.var] += 1
				print(CM.Player.potions)
				return "You picked up the {}".format(thing.itemType)
			else:
				CM.Player.pack[takeItem]=thing
				return "You picked up the {0} {1}".format(takeItem,\
					thing.itemType)
		else:
			return "There is no {} here".format(takeItem)
	else:
		return "Need target to take"


def getInput():
	command = input(": ").split()
	verbIn = command[0].lower()
	if verbIn in verbDict:
		verb = verbDict[verbIn]
	else:
		print("Unknown verb {}".format(verbIn))
		return 0
	if verbIn.lower() == 'quit':
		return quitGame()
	else:
		if len(command)>=2:
			nounIn = command[1].lower()
			if nounIn == pName or nounIn.lower() == 'self':
				nounIn = 'you'
			print(verb(nounIn))
		else:
			print(verb())
		return 0


def help(vHelp = None):
	"""Return descriptions on various actions"""
	helpMsg = " "
	helpStr = "{0:10s} -{1:20s}\n"
	if(vHelp != None):
		if(vHelp in verbDict):
			helpMsg = helpStr.format(vHelp,verbDict[vHelp].__doc__)
		else:
		# verb not found in dictionary, return verbs with same first letter
			helpMsg = 'No specific action "{}"'.format(vHelp)+'\n'
			for key in sortedVerbs:
				if(vHelp[0]==key[0]):
					helpMsg += helpStr.format(key,verbDict[key].__doc__)
	else:
		for key in sortedVerbs:
			helpMsg += helpStr.format(key,verbDict[key].__doc__)
	return helpMsg.strip()


def equip(equipObj = None):
	"""Equip an object from your pack"""
	equipStr = "You equiped the "
	if(equipObj == None):
		return 'Need target to equip'
	else:
		if equipObj in CM.Player.pack:
			thing = CM.Player.pack[equipObj]
			eStr = IM.allAdj[IM.inRare(equipObj)][equipObj]
			# string to enhance attribute
			if (thing.equipSlot[0] == 'a'):
				if (len(CM.Player.arms)<=2):
					CM.Player.arms[equipObj] = thing
					del(CM.Player.pack[equipObj])
					CM.GameCharacter.objects['you'].valEnhance(eStr,0)
					return equipStr+"{0} {1}".\
						format(thing.itemName,thing.itemType)
				else:
					return equipFull('arms')
			elif(thing.equipSlot[0] == 'l'):
				if(len(CM.Player.legs)<=2):
					CM.Player.legs[equipObj] = thing
					CM.GameCharacter.objects['you'].valEnhance(eStr,0)
					del(CM.Player.pack[equipObj])
					return equipStr+"{0} {1}".\
						format(thing.itemName,thing.itemType)
				else:
					return equipFull('legs')
			elif(thing.equipSlot[0] == 'h'):
				if(len(CM.Player.head)<=1):
					CM.Player.head[equipObj] = thing
					CM.GameCharacter.objects['you'].valEnhance(eStr,0)
					del(CM.Player.pack[equipObj])
					return equipStr+"{0} {1}".\
						format(thing.itemName,thing.itemType)
				else:
					return equipFull('head')
		else:
			return "No item {} in pack.".format(equipObj)


def equipFull(equipSlot):
	"""Error message for equipping an item to a full slot"""
	return "{} full. Need to drop an item.".format(equipSlot.capitalize())


def unequip(item = None):
	"""Unequip an item and place it in your pack"""
	if item != None:
		eStr = IM.allAdj[IM.inRare(item)][item]
		if item in CM.Player.arms:
			itemCls = CM.Player.arms[item]
			del CM.Player.arms[item]
			# eStr = IM.allAdj[IM.inRare(item)][item]
			CM.GameCharacter.objects['you'].valEnhance(eStr,1)
			CM.Player.pack[item] = itemCls
			return "You unequipped the {} {}.".\
				format(item,itemCls.itemType)
		elif item in CM.Player.legs:
			itemCls = CM.Player.legs[item]
			del CM.Player.head[item]
			# eStr = IM.allAdj[item]
			CM.GameCharacter.objects['you'].valEnhance(eStr,1)
			CM.Player.pack[item] = itemCls
			return "You unequipped the {} {}.".\
				format(item,itemCls.itemType)
		elif item in CM.Player.head:
			itemCls = CM.Player.head[item]
			del CM.Player.head[item]
			# eStr = IM.allAdj[item]
			CM.GameCharacter.objects['you'].valEnhance(eStr,1)
			CM.Player.pack[item] = itemCls
			return "You unequipped the {} {}.".\
				format(item,itemCls.itemType)
		else:
			return "Item {} not equipped.".format(item)
	else:
		return "Need target to unequip/"

def move(direction = None):
	"""Select a compass direction (NSEW) to move the player"""
	curSwp = CM.getLoc()
	curPos = RM.sweepFunc(curSwp)
	nbors = {}	# keys: valid directions; values: corresponding room
	# North
	if validCoord(curPos[1]+1,1):
		nbors['north'] = RM.sweepFunc(curPos[0],curPos[1]+1)
	if validCoord(curPos[1]-1,1):
		nbors['south'] = RM.sweepFunc(curPos[0],curPos[1]-1)
	if validCoord(curPos[0]-1,0):
		nbors['west'] = RM.sweepFunc(curPos[0]-1,curPos[1])
	if validCoord(curPos[0]+1,0):
		nbors['east'] = RM.sweepFunc(curPos[0]+1,curPos[1])
	if direction == None:
		mvStr = 'Possible directions:\n'
		if 'north' in nbors:
			mvStr += 'North\n'
		if 'east' in nbors:
			mvStr += 'East\n'
		if 'south' in nbors:
			mvStr += 'South\n'
		if 'west' in nbors:
			mvStr += 'West'
			return mvStr
		else:
			return mvStr.strip()
	elif direction.lower() in ['north','south','east','west']:
		d = direction.lower()
		if d in nbors:
			toSwp = nbors[d]
			toPos = RM.sweepFunc(toSwp)
			# RM.addToRoom('you',toSwp)
			# RM.delFromRoom('you',curSwp)
			RM.rooms[toSwp].enemies['you'] = CM.GameCharacter.objects['you']
			del RM.rooms[curSwp].enemies['you']
			del CM.Player.pos[curSwp]
			CM.Player.pos[toSwp] = RM.rooms[toSwp]
			return 'Moved from {0} to {1}'.format(curPos,toPos)
		else:
			return 'No door in that direction.'
	else:
		return "{} is not a valid direction of movement.".format(direction.capitalize())

def validCoord(curcoord,dim):
	"""Returns true if curcoord within gamespace dimension dim"""
	# dim == 0 => x, dim == 1 => y
	if curcoord > 0:
		if dim == 0: # moving in x
			if curcoord <= RM.roomsX:
				return True
			else:
				return False
		elif dim == 1: # moving in y
			if curcoord <= RM.roomsY:
				return True
			else:
				return False
		else:
			raise SystemExit('Bad Dimension in validCoord')
	else:
		return False


def quitGame(val = None):
	"""Quit the game"""
	print('You are about to quit the game. If you do so, you will lose'+\
		' all progress.\nAre you sure you want to do this?\n')
	quitVal = str(input('Press y to quit\n: '))
	if quitVal.lower() == 'y':
		# print('Until next time, brave adventurer.')
		raise SystemExit('Until next time, brave adventurer.')
	else:
		print('Carry on!')
		return 0


# Verb Dictionary
verbDict = {
	"say": say,
	"examine": examine,
	"hit": hit,
	"help": help,
	"take": take,
	"equip": equip,
	"move": move,
	"quit": quitGame,
	"unequip": unequip,
	"drink":drink,
}
sortedVerbs = sorted(verbDict)

pName = ""
