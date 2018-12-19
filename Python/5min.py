# Challenges
#from challenges.basic import Basic
#from challenges.level import Level

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



LOWEST_SLEEP_TO_KILL = 3.8
ADVENTURE_ZONE = {0: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
				  1: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
				  2: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
				  3: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
				  4: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": 4.1},
				  5: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": 8},
				  6: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": 9}}
MAX_KILL_ADVENTURE_ZONE = 5 #if you only want to kill up towards "Mega Lands" enter 5 and it will avoid Beardverse and onwards


def intTryParse(value):
	try:
		return int(value)
	except ValueError:
		return 0

def kill_bosses(currentBoss, timeSinceStart, GoldClearLevels):
	room = 0
	newBossToKill = False

	for i in range(MAX_KILL_ADVENTURE_ZONE,-1,-1):
		if GoldClearLevels >= i:
			break
		if currentBoss > ADVENTURE_ZONE[i]["boss"]:
			highestBoss = currentBoss < ADVENTURE_ZONE[i + 1]["boss"] #Could be better with <= but then there is a rare bug where the game has killed one more boss since the last CurrentBoss was grabbed
			
			feature.loadout(1)  # Gold drop equipment
			if timeSinceStart >= 100: #before 100sec the game does not have the ability to manually attack
				feature.snipe(ADVENTURE_ZONE[i]["floor"], 999, once=True, highest=highestBoss, bosses=True)
			else:
				feature.adventure(zone=ADVENTURE_ZONE[i]["floor"], highest=highestBoss)
				time.sleep(ADVENTURE_ZONE[i]["sleep"])
			feature.loadout(2)  # Bar/power equimpent

			return True, i
	return False, 0

def Nov_SpeedRun_Two(duration, counter):
	currentBoss = 0
	GoldClearLevels = -1
	TM_Done = False
	Aug_Assigned = False
	Blood_Assigned = False
	Digger_Activated = False
	#ONLY_DO_ONCE = False
	half_energy_WANDOOS = False
	
	
	feature.do_rebirth()
	start = time.time()
	end = time.time() + (duration * 60) + 1

	feature.nuke() #67 = Clock Dimension, #75 = The2DUniverse, #83 = AncientBattlefield
	time.sleep(2)
	feature.augments({"SS": 0.8, "DS": 0.2}, 1e6)

	while time.time() < (end - 10): 
		feature.nuke()
		feature.fight()
		currentBoss = intTryParse(feature.get_current_boss())
		
		var1, var2 = kill_bosses(currentBoss, time.time() - start, GoldClearLevels)
		if var1:
			feature.adventure(itopod=True, itopodauto=True)
			GoldClearLevels = var2
		'''
		if time.time() > (start + 100) and not ONLY_DO_ONCE:
			ONLY_DO_ONCE = True
			GoldClearLevels -= 1
		'''
		if (start + duration * 60 * 0.25) > time.time() and not TM_Done: #the first 25% of the run
			feature.time_machine(1e9, magic=True)
		else:
			if not TM_Done:
				nav.menu("timemachine")
				i.click(570,235)
				i.click(570,335)
				TM_Done = True

			if not Digger_Activated:
				feature.NOV_gold_diggers([2,5], [20,1], activate=True)
				Digger_Activated = True

			if not Aug_Assigned:
				nav.menu("augmentations")
				time.sleep(1) #For some fucking reason this one buggs out without a sleep here
				feature.augments({"SS": 0.565, "DS": 0.435}, 39e6)
				#time.sleep(5)
				Aug_Assigned = True
				
			if not Blood_Assigned:
				nav.menu("bloodmagic")
				i.click(ncon.BMX, ncon.BMY[3])
				Blood_Assigned = True
			
			feature.wandoos(True)
			if not half_energy_WANDOOS:
				idle_color = i.get_pixel_color(426, 250)
				if idle_color == "59CF81":
					half_energy_WANDOOS = True
			else:
				feature.assign_ngu(1e9, [1])

		#feature.NOV_boost_equipment("weapon")
		feature.NOV_boost_equipment("cube")
		time.sleep(1)
		#feature.boost_equipment() #boostar också Cube
	
	if counter != 0:
		nav.menu("augmentations")
		i.click(10, 10)
		aaa = i.get_bitmap()
		aaa.save("Pic\\augment" + str(counter) + ".png")
	
	#nav.reclaim_all_magic()
	nav.reclaim_all_energy()
	feature.speedrun_bloodpill()
	
	if Digger_Activated:
		feature.gold_diggers([2,5], activate=True)
	feature.gold_diggers([3], activate=True)
	feature.nuke()
	feature.fight()
	time.sleep(1)
	feature.pit()
	feature.spin()
	feature.save_check()
	tracker.progress()
	#u.em()
	#tracker.adjustxp()
	
	while time.time() < end:
		time.sleep(0.1)
	
	if counter != 0:
		nav.rebirth()
		i.click(10, 10)
		aaa = i.get_bitmap()
		aaa.save("Pic\\rebirth" + str(counter) + ".png")


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 2, 2, 5) #Hur den ska spendare EXP inom Energy & Magic caps
print(w.x, w.y)
tracker = Tracker(7)		#Progress tracker int val = tid för run


#c = Challenge()
#print("Current challenge : " + str(c.check_challenge()))
#c.start_challenge(1)


#MENUITEMS = ["fight", "pit", "adventure", "inventory", "augmentations","advtraining", "timemachine", 
#				"bloodmagic", "wandoos", "ngu","yggdrasil", "digger", "beard"]
#EQUIPMENTSLOTS = {"accessory1","accessory2","accessory3","accessory4","accessory5","head","chest",
#"legs","boots","weapon","cube"} acc1=vänsterOmHelm,acc2=underAcc1,acc3=underAcc2



runCounter = 1
while True:
	#feature.NOV_snipe_hard(0, 300, highest=True, bosses=True)	# Equipment sniping
	#feature.snipe(13, 120, bosses=False)						# Boost Sniping
	#feature.merge_equipment()
	#feature.merge_inventory(17) #mergar de första 25 slotsen
	#feature.boost_inventory(1)
	#feature.boost_equipment() #boostar också Cube
	#feature.ygg()
	
	
	#Börja använda Magic beard digger när jag har GPS till det
	#använd blood magic Gold upgrade för några sec
	
	
	Nov_SpeedRun_Two(7, 0)
	#Beard	=	The Fu manchu
	#Blood	=	Blood numbers boost
	#TM		=	0/0
	runCounter += 1