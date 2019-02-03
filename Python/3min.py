# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import NOV_Tracker
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time

LOWEST_SLEEP_TO_KILL = 3.30
ADVENTURE_ZONE = {0: {"name": "Cave of Many Things", "boss": 37, "floor": 4, "sleep": LOWEST_SLEEP_TO_KILL},
				  1: {"name": "The Sky", "boss": 48, "floor": 5, "sleep": LOWEST_SLEEP_TO_KILL},
				  2: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
				  3: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
				  4: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
				  5: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
				  6: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": LOWEST_SLEEP_TO_KILL},
				  7: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": LOWEST_SLEEP_TO_KILL},
				  8: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": LOWEST_SLEEP_TO_KILL},
				  9: {"name": "Badly Drawn World", "boss": 116, "floor": 18, "sleep": LOWEST_SLEEP_TO_KILL},
				  10: {"name": "Boring-Ass Earth", "boss": 124, "floor": 19, "sleep": 5},
				  11: {"name": "Chocolate World", "boss": 137, "floor": 21, "sleep": 9}}
MAX_KILL_ADVENTURE_ZONE = 10 # 6 if you only want to kill up towards "Mega Lands", no more
SCREENSHOT_BOOLEAN = {"aug" : {"Use" : False, "Menu" : "augmentations"},
					  "TM" : {"Use" : False, "Menu" : "timemachine"},
					  "blood" : {"Use" : False, "Menu" : "bloodmagic"},
					  "wandoos" : {"Use" : False, "Menu" : "wandoos"},
					  "ngu" : {"Use" : False, "Menu" : "ngu"},
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
	GoldClearLevels = 0
	Blood_Assigned = False
	WANDOOS_energy_goal_reached = False
	WANDOOS_magic_goal_reached = False
	Augment_Assigned = False
	XP_Digger = False
	BB_NGU = False
		
	feature.do_rebirth()
	start = time.time()
	end = time.time() + (duration * 60)

	
	feature.nuke(101)
	currentBoss = feature.get_current_boss_two()
	feature.adventure(highest=True)
	feature.time_machine(190e6, 250e6)
	feature.augments({"SM": 1}, 400e6)
	feature.augments({"AA": 1}, 130e6)

	while time.time() < (end - 11):
		if XP_Digger:
			feature.nuke()
			feature.fight()
			currentBoss = feature.get_current_boss_two()
		
		if time_since_start() < 60:
			var1, var2 = kill_bosses(currentBoss, 0, GoldClearLevels)
			if var1:
				feature.adventure(itopod=True, itopodauto=True)
				GoldClearLevels = var2

		if not Blood_Assigned:
			feature.blood_magic(8)
			Blood_Assigned = True
			
		if not Augment_Assigned:
			#feature.augments({"SM": 1}, 200e6)
			#feature.augments({"AA": 1}, 30e6)
			Augment_Assigned = True

		if time_since_start() > 150 and not XP_Digger:
			feature.deactivate_all_diggers()
			feature.gold_diggers([12])
			feature.gold_diggers([2,5,6,9])
			XP_Digger = True
		else:
			feature.gold_diggers([2,5,6,9,12])

		feature.wandoos(True)

		if not WANDOOS_energy_goal_reached:
			idle_color = i.get_pixel_color(525, 250)
			#100% = 525, 50% = 426, 33% = 393, 25% = 376, 20% = 366, (1/6)% = 359, (1/7)% = 355
			if idle_color == "59CF81":
				WANDOOS_energy_goal_reached = True

		if not WANDOOS_magic_goal_reached:
			idle_color = i.get_pixel_color(525, 350)
			#100% = 525, 50% = 426, 33% = 393, 25% = 376, 20% = 366, (1/6)% = 359, (1/7)% = 355
			if idle_color == "A9BAF9":
				WANDOOS_magic_goal_reached = True

		if WANDOOS_energy_goal_reached:
			if not BB_NGU:
				feature.bb_ngu(1e9, [1], 1.02)
				BB_NGU = True
			feature.assign_ngu(1e12, [2])
				
		if WANDOOS_magic_goal_reached:
			feature.assign_ngu(1e12, [3], magic=True)

	debugScreenShot("TM", counter)
	debugScreenShot("aug", counter)
	debugScreenShot("blood", counter)
	debugScreenShot("wandoos", counter)

	feature.NOV_boost_equipment("accessory1")
	feature.NOV_boost_equipment("cube")
	
	feature.pit(value=1e24)
	feature.speedrun_bloodpill()
	
	feature.deactivate_all_diggers()
	feature.gold_diggers([3,12])
	feature.nuke()
	feature.fight()
	feature.spin()
	feature.save_check()
	tracker.update_progress()

	debugScreenShot("rebirth", counter)
	debugScreenShot("ngu", counter)
	
	while time.time() < (end - 0.5):
		time.sleep(0.1)
	feature.stop_fight()
	

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 2, 2, 2)
print(w.x, w.y)
tracker = NOV_Tracker()

#MENUITEMS = ["fight", "pit", "adventure", "inventory", "augmentations","advtraining", "timemachine", 
#				"bloodmagic", "wandoos", "ngu","yggdrasil", "digger", "beard", "settings"]
#EQUIPMENTSLOTS = {"accessory1","accessory2","accessory3","accessory4","accessory5","head","chest",
#"legs","boots","weapon","cube"} acc1=vänsterOmHelm,acc2=underAcc1,acc3=underAcc2




runCounter = 1
while True:
	"""
	Rätt beard (1,3,4)
	Rätt Blood Auto(Number / Gold)
	"""
	Nov_SpeedRun_Two(3, runCounter)
	if runCounter % 10 == 0:
		u.em()
		tracker.adjustxp()
	runCounter += 1