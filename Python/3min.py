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


LOWEST_SLEEP_TO_KILL = 3.40
ADVENTURE_ZONE = {0: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
				  1: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
				  2: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
				  3: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
				  4: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": LOWEST_SLEEP_TO_KILL},
				  5: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": LOWEST_SLEEP_TO_KILL},
				  6: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": 5},
				  7: {"name": "Badly Drawn World", "boss": 116, "floor": 18, "sleep": 9},
				  8: {"name": "Boring-Ass Earth", "boss": 124, "floor": 19, "sleep": 9}}
MAX_KILL_ADVENTURE_ZONE = 5 #if you only want to kill up towards "Mega Lands" enter 5 and it will avoid Beardverse and onwards
SCREENSHOT_BOOLEAN = {"aug1" : {"Use" : False, "Menu" : "augmentations"},
					  "aug2" : {"Use" : False, "Menu" : "augmentations"},
					  "blood" : {"Use" : False, "Menu" : "bloodmagic"},
					  "wandoos" : {"Use" : False, "Menu" : "wandoos"},
					  "rebirth" : {"Use" : False}}



def debugScreenShot(name, counter):
	if SCREENSHOT_BOOLEAN[name]["Use"]:
		if name == "rebirth":
			nav.rebirth()
		else:
			nav.menu(SCREENSHOT_BOOLEAN[name]["Menu"])
		i.click(10, 10)
		aaa = i.get_bitmap()
		aaa.save("Pic\\" + name + "_" + str(counter) + ".png")

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

	def time_since_start():
		return time.time() - start

	currentBoss = 0
	GoldClearLevels = 4
	TM_Done = False
	Aug_Assigned = False
	Blood_Assigned = False
	Digger_Activated = False
	WANDOOS_energy_goal_reached = False
	WANDOOS_magic_goal_reached = False
	
	testVar = 0
	
	feature.do_rebirth()
	start = time.time()
	end = time.time() + (duration * 60)

	feature.nuke() #67 = Clock Dimension, #75 = The2DUniverse, #83 = AncientBattlefield
	time.sleep(1.7)
	feature.adventure(highest=True)
	feature.time_machine(39e6, magic=True)
	feature.augments({"CI": 1}, 26e6)
	feature.augments({"ML": 1}, 13e6)

	while time.time() < (end - 14): 
		feature.nuke()
		feature.fight()
		currentBoss = intTryParse(feature.get_current_boss())
		
		if time_since_start() < 35:
			var1, var2 = kill_bosses(currentBoss, 0, GoldClearLevels)
			if var1:
				feature.adventure(itopod=True, itopodauto=True)
				GoldClearLevels = var2

		if testVar < 2 and GoldClearLevels == 5:
			feature.wandoos(False)
			testVar += 1
		
		if (start + duration * 60 * 0.20) > time.time(): #the first 25% of the run
			feature.time_machine(1e12, magic=True)
		else:
			if not TM_Done:
				nav.menu("timemachine")
				i.click(570,235)
				i.click(570,335)
				
				#nav.input_box()
				#i.NOV_send_text(20e6)
				#i.click(ncon.TMSPEEDX, ncon.TMSPEEDY)
				TM_Done = True

			if not Aug_Assigned:
				debugScreenShot("aug1", counter)

				feature.augments({"CI": 1}, 86e6)
				feature.augments({"ML": 1}, 44e6)
				Aug_Assigned = True
			
			if not Blood_Assigned:
				#nav.menu("bloodmagic")
				#i.click(ncon.BMX, ncon.BMY[4])
				
				feature.blood_magic(5)
				
				nav.input_box()
				i.NOV_send_text(25.1e6)
				i.click(ncon.BMX - 75, ncon.BMY[5])
				Blood_Assigned = True
			
			feature.wandoos(True)

			if not WANDOOS_energy_goal_reached:
				idle_color = i.get_pixel_color(525, 250)
				#100% = 525, 50% = 426, 33% = 393, 25% = 376, 20% = 366, (1/6)% = 359, (1/7)% = 355
				if idle_color == "59CF81":
					WANDOOS_energy_goal_reached = True

			if not WANDOOS_magic_goal_reached:
				idle_color = i.get_pixel_color(426, 350)
				#100% = 525, 50% = 426, 33% = 393, 25% = 376, 20% = 366, (1/6)% = 359, (1/7)% = 355
				if idle_color == "A9BAF9":
					WANDOOS_magic_goal_reached = True

			if WANDOOS_energy_goal_reached:
				feature.assign_ngu(1e12, [1])
				
			if WANDOOS_magic_goal_reached:
				feature.assign_ngu(1e12, [3], magic=True)

			if not Digger_Activated:
				feature.NOV_gold_diggers([2,5,6,8], [43,19,19,7], activate=True)
				Digger_Activated = True


	debugScreenShot("aug2", counter)
	debugScreenShot("blood", counter)
	debugScreenShot("wandoos", counter)
	
	aaa = i.get_bitmap()
	aaa.save("Pic\\money_" + str(counter) + ".png")
	
	feature.NOV_boost_equipment("weapon")
	feature.NOV_boost_equipment("cube")
	
	#nav.reclaim_all_magic()
	#nav.reclaim_all_energy()
	feature.speedrun_bloodpill()
	
	if Digger_Activated:
		feature.gold_diggers([2,5,6,8], deactivate=True)
	feature.gold_diggers([3])
	feature.nuke()
	feature.fight()
	time.sleep(1)
	feature.pit(value=1e21)
	feature.spin()
	feature.save_check()
	tracker.progress()
	#u.em()
	#tracker.adjustxp()
	
	feature.loadout(1)  # Gold drop equipment. in order to start with gold gear next run
	while time.time() < end:
		time.sleep(0.1)
	
	debugScreenShot("rebirth", counter)


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 3, 3, 10) #Hur den ska spendare EXP inom Energy & Magic caps
print(w.x, w.y)
tracker = Tracker(3)		#Progress tracker int val = tid för run

#MENUITEMS = ["fight", "pit", "adventure", "inventory", "augmentations","advtraining", "timemachine", 
#				"bloodmagic", "wandoos", "ngu","yggdrasil", "digger", "beard", "settings"]
#EQUIPMENTSLOTS = {"accessory1","accessory2","accessory3","accessory4","accessory5","head","chest",
#"legs","boots","weapon","cube"} acc1=vänsterOmHelm,acc2=underAcc1,acc3=underAcc2




runCounter = 1
while True:
	Nov_SpeedRun_Two(3, runCounter)
	runCounter += 1