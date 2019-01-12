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

BOSSES = {0: {"LootGear": False, "TimeToKill": 0, "NewTime": "1:0"},
			1: {"LootGear": True, "TimeToKill": 0, "NewTime": "1:57"},
			2: {"LootGear": True, "TimeToKill": 0, "NewTime": "2:57"}}


def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

def createTimeStamp(boss, timeLeft, SafetyTime = 60):
	split = timeLeft.split(":")
	BOSSES[boss]["TimeToKill"] = time.time() + int(split[0]) * 3600 + int(split[1]) * 60
	BOSSES[boss]["TimeToKill"] += SafetyTime
	
def timeToKillBoss(Boss_ID):
	if BOSSES[Boss_ID]["LootGear"]:
		print("Equipping loot gear")
		nav.reclaim_all_magic()
		nav.reclaim_all_energy()
		feature.gold_diggers([5,6], activate=True) #Disable NGU Diggers
		feature.gold_diggers([1,4], activate=True) #Enable Drop & Adventure digger
		feature.loadout(3) #Equip dropchance Gear
	
	nav.menu("settings")
	i.click(670, 150) #Enable "Loot Filter"
	i.click(510, 290) #Enable "Auto Kill Titans"
	time.sleep(1)

	createTimeStamp(Boss_ID, BOSSES[Boss_ID][NewTime], SafetyTime = 5)
	i.click(580, 290) #Disable "Auto Kill Titans"
	i.click(740, 150) #Disable "Loot Filter"
	
	if BOSSES[Boss_ID]["LootGear"]:
		print("Equipping NGU gear")
		feature.gold_diggers([1,4], activate=True) #Disable Drop & Adventure digger
		feature.gold_diggers([5,6], activate=True) #Enable NGU Diggers
		feature.loadout(2) #Equip EM POW Gear
			
		for abcccccc in range(4):
			feature.assign_ngu(1e9, [1])
			feature.assign_ngu(1e9, [3], magic=True)
			time.sleep(2)


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 3, 3, 10) #Hur den ska spendare EXP inom Energy & Magic caps
print(w.x, w.y)


SwitchToDropGear = False
createTimeStamp(0,"9:5")
createTimeStamp(1,"9:48")
createTimeStamp(2,"9:53")




if SwitchToDropGear:
	nav.menu("settings")
	i.click(580, 290) #Disable "Auto Kill Titans"

while True:
	feature.NOV_snipe_hard(0, 300, highest=True, bosses=True)	# Equipment sniping
	#feature.snipe(13, 120, bosses=False)						# Boost Sniping
	
	feature.merge_equipment()
	#feature.merge_inventory(13) #mergar de första 25 slotsen
	
	#feature.boost_inventory(1)
	#feature.boost_equipment() #boostar också Cube
	#feature.NOV_boost_equipment("head")
	
	feature.ygg()
	feature.pit()
	if feature.speedrun_bloodpill():
		nav.reclaim_all_energy()
		nav.reclaim_all_magic()
	feature.spin()
	feature.save_check()	
	
	feature.assign_ngu(1e12, [1])
	feature.assign_ngu(1e12, [3], magic=True)
	
	if SwitchToDropGear:
		#clearConsole()
		for BossID in range(len(BOSSES)):
			#duration = int(BOSSES[BossID]["TimeToKill"] - time.time())
			#hour = int(duration / 3600)
			#min  = int((duration - hour * 3600) / 60)
			#print(f"Time left to kill boss {BossID} - {hour}:{min}")
			
			if BOSSES[BossID]["TimeToKill"] < time.time():
				timeToKillBoss(BossID)