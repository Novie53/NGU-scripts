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

LOWEST_SLEEP_TO_KILL = 3.40
ADVENTURE_ZONE = {0: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
				  1: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
				  2: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
				  3: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
				  4: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": LOWEST_SLEEP_TO_KILL},
				  5: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": LOWEST_SLEEP_TO_KILL},
				  6: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": LOWEST_SLEEP_TO_KILL},
				  7: {"name": "Badly Drawn World", "boss": 116, "floor": 18, "sleep": 9},
				  8: {"name": "Boring-Ass Earth", "boss": 124, "floor": 19, "sleep": 9}}
MAX_KILL_ADVENTURE_ZONE = 6 #if you only want to kill up towards "Mega Lands" enter 5 and it will avoid Beardverse and onwards
SCREENSHOT_BOOLEAN = {"aug" : {"Use" : True, "Menu" : "augmentations"},
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
		aaa.save("Pic\\debug_" + name + "_" + str(counter) + ".png")

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
		
	feature.do_rebirth()
	start = time.time()
	end = time.time() + (duration * 60)

	feature.nuke() #67 = Clock Dimension, #75 = The2DUniverse, #83 = AncientBattlefield
	time.sleep(1.7)
	feature.adventure(highest=True)
	feature.time_machine(100e6, magic=True)
	feature.augments({"CI": 1}, 114e6)
	feature.augments({"ML": 1}, 52e6)

	while time.time() < (end - 12): 
		feature.nuke()
		feature.fight()
		currentBoss = intTryParse(feature.get_current_boss())
		
		var1, var2 = kill_bosses(currentBoss, 0, GoldClearLevels)
		if var1:
			feature.adventure(itopod=True, itopodauto=True)
			GoldClearLevels = var2

		if not Blood_Assigned and time_since_start() > 15:
			feature.blood_magic(6)
			#nav.input_box()
			#i.NOV_send_text(20e6)
			#i.click(ncon.BMX - 75, ncon.BMY[6])
			Blood_Assigned = True

		if not Digger_Activated and time_since_start() > 35:
			feature.NOV_gold_diggers([2,5,6,8], [-1,-1,-1,-1], activate=True)
			Digger_Activated = True

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
			feature.assign_ngu(1e12, [1])
				
		if WANDOOS_magic_goal_reached:
			feature.assign_ngu(1e12, [3], magic=True)


	debugScreenShot("aug", counter)
	debugScreenShot("blood", counter)
	debugScreenShot("wandoos", counter)

	feature.NOV_boost_equipment("boots")
	feature.NOV_boost_equipment("cube")
	
	feature.pit(value=1e24)
	feature.speedrun_bloodpill()
	
	feature.deactivate_all_diggers()
	feature.gold_diggers([3])
	feature.nuke()
	feature.fight()
	time.sleep(1)
	feature.spin()
	feature.save_check()
	tracker.progress()

	
	debugScreenShot("rebirth", counter)
	
	while time.time() < end:
		time.sleep(0.1)



w = Window(debug=True)
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 3, 3, 10) #Hur den ska spendare EXP inom Energy & Magic caps
print(w.x, w.y)
#tracker = NOV_Tracker()

#MENUITEMS = ["fight", "pit", "adventure", "inventory", "augmentations","advtraining", "timemachine", 
#				"bloodmagic", "wandoos", "ngu","yggdrasil", "digger", "beard", "settings"]
#EQUIPMENTSLOTS = {"accessory1","accessory2","accessory3","accessory4","accessory5","head","chest",
#"legs","boots","weapon","cube"} acc1=vänsterOmHelm,acc2=underAcc1,acc3=underAcc2


feature.questing()
exit()



c = Challenge()
ScriptStart = time.time()
runCounter = 0
while True:
	feature.NOV_boost_equipment("cube")
	before = time.time()
	c.start_challenge(7)
	duration = time.time() - before # sec
	runCounter += 1
	
	min = int(duration / 60)
	sec = int(duration - min * 60)
	sec = sec if sec > 9 else "0" + str(sec)
	
	print(f"The challenge took {min}:{sec} minutes to complete")
	
	
	duration = time.time() - ScriptStart # sec
	hours = int(duration / 3600)
	min = int((duration - (hours * 3600)) / 60)
	min = min if min > 9 else "0" + str(min)
	print(f"Has completed {runCounter} challenges in the span of {hours}:{min} hours")
	print("----------------------------------")

	"""
	Rätt beard (1,3,4)
	Rätt Blood Auto(Number / Gold)
	Diggers[2,5,6,8], [52,25,25,13]
	"""
	#Nov_SpeedRun_Two(3, runCounter)
	#runCounter += 1