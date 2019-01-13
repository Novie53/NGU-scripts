# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time
import os



TITANS = {#"GRB": {"LootGear": False, "KillTime": 0},
		  #"GCT": {"LootGear": False, "KillTime": 0},
		  "jake": {"LootGear": True, "KillTime": 0},
		  #"UUG": {"LootGear": True, "KillTime": 0},
		  "walderp": {"LootGear": True, "KillTime": 0},
		  "BEAST1": {"LootGear": True, "KillTime": 0}}


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
	
def kill_Titans(timeToWait):
	while True:
		DropChanceEquipment = False
		LetsKillSomeBitches = False
		KillList = []
	
		for BossID in TITANS.keys():
			duration = int(TITANS[BossID]["KillTime"] - time.time())
			if duration <= timeToWait:
				print("Lets Kill: " + BossID)
				LetsKillSomeBitches = True
				DropChanceEquipment = DropChanceEquipment or TITANS[BossID]["LootGear"]
				KillList.append(BossID)

		if LetsKillSomeBitches:
			if DropChanceEquipment:
				print("Equipping loot gear")
				nav.reclaim_all_magic()
				nav.reclaim_all_energy()
				feature.loadout(3) #Equip dropchance Gear

			for x in KillList:
				while int(TITANS[x]["KillTime"] - time.time()) <= timeToWait:
					createTimeStamp(x, feature.kill_titan(x))

			if DropChanceEquipment:
				print("Equipping NGU gear")
				feature.loadout(2) #Equip EM POW Gear

				for abcccccc in range(4):
					feature.assign_ngu(1e12, [1])
					feature.assign_ngu(1e12, [3], magic=True)
					time.sleep(2)
		else:
			break

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
#print(w.x, w.y)




#settings
FarmInZoneDuration = 120




durationOffset = 0
durationOffsetTotal = 0
durationOffsetCount = 0

for x in TITANS.keys():
	createTimeStamp(x, feature.kill_titan(x))

while True:
	printTimeLeftToBoss()
	kill_Titans(FarmInZoneDuration + 30)

	
	tempZoneDuration = FarmInZoneDuration - durationOffset
	before = time.time()
	feature.snipe_hard(18, tempZoneDuration, highest=False, mobs=1, attackType=2)	# Equipment sniping
	print(str(int(time.time() - before)))
	durationOffsetTotal += (time.time() - before) - tempZoneDuration
	durationOffsetCount += 1
	durationOffset = round(durationOffsetTotal / durationOffsetCount, 2)

	
	nav.menu("inventory")
	aaa = i.get_bitmap()
	aaa.save("Pic\\longInv_" + str(durationOffsetCount) + ".png")
	feature.merge_equipment()
	feature.merge_inventory(9) #mergar de första 25 slotsen
	
	#feature.boost_inventory(1)
	#feature.boost_equipment() #boostar också Cube
	feature.NOV_boost_equipment("legs")
	feature.NOV_boost_equipment("cube")
	
	feature.ygg()
	feature.pit()
	if feature.speedrun_bloodpill():
		nav.reclaim_all_energy()
		nav.reclaim_all_magic()
	feature.spin()
	feature.save_check()	
	
	feature.assign_ngu(1e12, [1])
	feature.assign_ngu(1e12, [3], magic=True)