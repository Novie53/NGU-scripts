# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time
import os


TITANS = {#"GRB": {"LootGear": False, "KillTime": 0},
		  #"GCT": {"LootGear": False, "KillTime": 0},
		  #"jake": {"LootGear": True, "KillTime": 0},
		  #"UUG": {"LootGear": True, "KillTime": 0},
		  #"walderp": {"LootGear": True, "KillTime": 0, "ManualKill":False, "BaseCoolDown":180},
		  "BEAST1": {"LootGear": True, "KillTime": 0, "ManualKill":True, "BaseCoolDown":210}}


def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

def createTimeStamp(TITAN, timeLeft):
	if timeLeft is None:
		TITANS[TITAN]["KillTime"] = time.time()
		return

	timeSplit = timeLeft.split(":")
	if len(timeSplit) == 3:
		sec = int(timeSplit[0]) * 3600 + int(timeSplit[1]) * 60 + int(timeSplit[2])
	elif len(timeSplit) == 2:
		sec = int(timeSplit[0]) * 60 + int(timeSplit[1])
	elif len(timeSplit) == 1:
		sec = 0
	
	TITANS[TITAN]["KillTime"] = time.time() + sec

def kill_Titans_Two(timeToWait):
	global current_Gear_Loadout

	DropChanceEquipment = False
	ManualKillList = []

	for BossID in TITANS.keys():
		duration = int(TITANS[BossID]["KillTime"] - time.time())
		
		if (duration + 10) < 0:
			realTitanCoolDown = TITANS[BossID]["BaseCoolDown"] - 3 * NoRebirth_Challenge_Count
			realTitanCoolDown = 60 if realTitanCoolDown < 60 else realTitanCoolDown
			TITANS[BossID]["KillTime"] += realTitanCoolDown * 60
		elif duration <= timeToWait:
			print("Lets Kill: " + BossID)
			DropChanceEquipment = DropChanceEquipment or TITANS[BossID]["LootGear"]
			if TITANS[BossID]["ManualKill"]:
				ManualKillList.append(BossID)
	
	if DropChanceEquipment and current_Gear_Loadout != DropChanceGear_Loadout:
		print("Equipping loot gear")
		nav.reclaim_all_magic()
		nav.reclaim_all_energy()
		feature.loadout(DropChanceGear_Loadout) #Equip dropchance Gear
		current_Gear_Loadout = DropChanceGear_Loadout
		
		feature.assign_ngu(1e12, [1])
		feature.assign_ngu(1e12, [3], magic=True)
	elif not DropChanceEquipment and current_Gear_Loadout != MainGear_Loadout:
		print("Equipping NGU gear")
		nav.menu("inventory")
		nav.reclaim_all_magic()
		nav.reclaim_all_energy()
		feature.loadout(MainGear_Loadout) #Equip dropchance Gear
		current_Gear_Loadout = MainGear_Loadout
		
		feature.assign_ngu(1e12, [1])
		feature.assign_ngu(1e12, [3], magic=True)

	NotInFarmZone = False
	for x in ManualKillList:
		NotInFarmZone = True
		print("Manually killing " + x)
		while int(TITANS[x]["KillTime"] - time.time()) <= timeToWait:
			createTimeStamp(x, feature.kill_titan(x))
	return NotInFarmZone

def printTimeLeftToBoss():
	TimeLeftToTitan = 9999
	nextTitan = ""
	
	for BossID in TITANS.keys():
		duration = int(TITANS[BossID]["KillTime"] - time.time())
		if duration < TimeLeftToTitan:
			TimeLeftToTitan = duration
			nextTitan = BossID
	hour = int(TimeLeftToTitan / 3600)
	min = int((TimeLeftToTitan - hour * 3600) / 60)
	sec = TimeLeftToTitan - hour * 3600 - min * 60
	
	min = min if min > 9 else "0" + str(min)
	sec = sec if sec > 9 else "0" + str(sec)
	print(f"Time left to next boss {nextTitan} - {hour}:{min}:{sec}")
	return TimeLeftToTitan


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")


#settings
FarmInZoneDuration = 120
NoRebirth_Challenge_Count = 36
ZoneToFarmIn = 21 #21 = Chocolate World, 19 = Boring-Ass Earth, 18 = Badly Drawn World
MainGear_Loadout = 2
DropChanceGear_Loadout = 3
diggers_Loadout = [4, 5, 6, 9, 10]#ITOPOD


#feature.kill_titan("BEAST1")
#exit()
	
while feature.questing():
	time.sleep(0.1)
#exit()

while False:
	#feature.merge_equipment()
	#feature.merge_inventory(8)
	#feature.boost_equipment(cube=False)
	#feature.boost_inventory(1)
	#feature.NOV_boost_equipment("accessory5")
	feature.NOV_boost_equipment("cube")
	
	#nav.menu("inventory")
	#inv_pos = feature.get_Inventory_Slot_Pos(15)
	#i.click(inv_pos[0], inv_pos[1], button="right")
		
	feature.snipe_hard(18, 120, highest=False, mobs=0, attackType=2, forceStay=True)


current_Gear_Loadout = 1
durationOffset = 0
durationOffsetTotal = 0
durationOffsetCount = 0


for x in TITANS.keys():
	createTimeStamp(x, feature.kill_titan(x))
	if int(TITANS[x]["KillTime"] - time.time()) <= 0:
		createTimeStamp(x, feature.kill_titan(x))

feature.adventure(itopod=True, itopodauto=True)
#feature.adventure(zone=ZoneToFarmIn)

while True:
	printTimeLeftToBoss()
	if kill_Titans_Two(FarmInZoneDuration + 30):
		#feature.adventure(zone=ZoneToFarmIn)
		feature.adventure(itopod=True, itopodauto=True)

	
	tempZoneDuration = FarmInZoneDuration - durationOffset
	before = time.time()
	feature.snipe_hard(ZoneToFarmIn, tempZoneDuration, highest=True, mobs=0, attackType=2, forceStay=True)
	durationOffsetTotal += (time.time() - before) - tempZoneDuration
	durationOffsetCount += 1
	durationOffset = round(durationOffsetTotal / durationOffsetCount, 2)

	#nav.menu("inventory")
	#i.click(10, 10)
	#aaa = i.get_bitmap()
	#aaa.save("Pic\\24h_" + str(int(time.time())) + ".png")

	#feature.merge_equipment()
	#feature.merge_inventory(4)
	
	#feature.boost_equipment(cube=False) #boostar också Cube
	#feature.boost_inventory(2)
	feature.NOV_boost_equipment("cube")
	
	
	
	feature.ygg()
	feature.pit()
	if feature.speedrun_bloodpill():
		nav.reclaim_all_energy()
		nav.reclaim_all_magic()
		feature.deactivate_all_diggers()
		feature.gold_diggers(diggers_Loadout)
	feature.spin()
	feature.save_check()	
	
	feature.assign_ngu(1e12, [8])
	feature.assign_ngu(1e12, [2], magic=True)