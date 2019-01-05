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




BOSSES = {0: {"LootGear": False, "TimeToKill": 0, "NewTime": "1:0"},
			1: {"LootGear": True, "TimeToKill": 0, "NewTime": "1:57"},
			2: {"LootGear": True, "TimeToKill": 0, "NewTime": "2:57"}}



def createTimeStamp(boss, timeLeft):
	split = timeLeft.split(":")
	BOSSES[boss]["TimeToKill"] = time.time() + int(split[0]) * 3600 + int(split[1]) * 60
	BOSSES[boss]["TimeToKill"] += 60
	
def timeToKillBoss(boss):
	if (time.time() - lastBossKill) > 600: #10 minutes
		nav.reclaim_all_magic()
		nav.reclaim_all_energy()
		feature.gold_diggers([5,6], activate=True) #Disable NGU Diggers
		feature.gold_diggers([1,4], activate=True) #Enable Drop & Adventure digger
		feature.loadout(3) #Equip dropchance Gear
		i.click(220, 465) #Settings Menu
		i.click(670, 150) #Enable "Loot Filter"
		i.click(510, 290) #Enable "Auto Kill Titans"
		time.sleep(1)
		
		i.click(580, 290) #Disable "Auto Kill Titans"
		i.click(740, 150) #Disable "Loot Filter"
		feature.gold_diggers([1,4], activate=True) #Disable Drop & Adventure digger
		feature.gold_diggers([5,6], activate=True) #Enable NGU Diggers
		feature.loadout(2) #Equip EM POW Gear
		
		for abcccccc in range(4):
			feature.assign_ngu(1e9, [1])
			feature.assign_ngu(1e9, [3], magic=True)
			time.sleep(2)
			
		lastBossKill = time.time()


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 3, 3, 10) #Hur den ska spendare EXP inom Energy & Magic caps
print(w.x, w.y)




createTimeStamp(0,"0:12")
createTimeStamp(1,"1:0")
createTimeStamp(2,"0:3")


#lastBossKill = time.time()
#i.click(220, 465) #Settings Menu
#i.click(580, 290) #Disable "Auto Kill Titans"


while True:
	#feature.NOV_snipe_hard(0, 300, highest=True, bosses=True)	# Equipment sniping
	#feature.snipe(13, 120, bosses=False)						# Boost Sniping
	feature.merge_equipment()
	feature.merge_inventory(14) #mergar de första 25 slotsen
	#feature.boost_inventory(1)
	feature.boost_equipment() #boostar också Cube
	#feature.NOV_boost_equipment("head")
	feature.ygg()
	feature.pit()
	
	for BossID in range(len(BOSSES)):
		if BOSSES[BossID]["TimeToKill"] < time.time():
			print(f"time to kill boss:{BossID}")
			input()
			timeToKillBoss(BossID)
			
			
	
	
