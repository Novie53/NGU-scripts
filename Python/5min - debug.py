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


LOWEST_SLEEP_TO_KILL = 3.75
ADVENTURE_ZONE = {0: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
				  1: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
				  2: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
				  3: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
				  4: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": 4.3},
				  5: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": 8},
				  6: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": 9}}
MAX_KILL_ADVENTURE_ZONE = 4 #if you only want to kill up towards "Mega Lands" enter 5 and it will avoid Beardverse and onwards


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
	GoldClearLevels = 2
	TM_Done = False
	Aug_Assigned = False
	Blood_Assigned = False
	Digger_Activated = False
	half_energy_WANDOOS = False
	
	
	feature.do_rebirth()
	start = time.time()
	end = time.time() + (duration * 60) + 1

	feature.nuke() #67 = Clock Dimension, #75 = The2DUniverse, #83 = AncientBattlefield
	time.sleep(1.8)
	feature.adventure(highest=True)
	feature.time_machine(1e9, magic=True)
	feature.augments({"SS": 0.8, "DS": 0.2}, 1e6)

	while time.time() < (end - 13): 
		feature.nuke()
		feature.fight()
		currentBoss = intTryParse(feature.get_current_boss())
		
		var1, var2 = kill_bosses(currentBoss, 0, GoldClearLevels)
		if var1:
			feature.adventure(itopod=True, itopodauto=True)
			GoldClearLevels = var2

		if (start + duration * 60 * 0.25) > time.time(): #the first 25% of the run
			feature.time_machine(1e9, magic=True)
		else:
			if not TM_Done:
				nav.menu("timemachine")
				i.click(570,235)
				i.click(570,335)
				TM_Done = True

			if not Digger_Activated:
				feature.NOV_gold_diggers([2,5], [22,4], activate=True)
				Digger_Activated = True

			if not Aug_Assigned:
				feature.augments({"MI": 1}, 30e6)
				i.click(575,265)
				i.click(570,290)
				feature.augments({"DTMT": 1}, 15e6)
				Aug_Assigned = True
			
			nav.menu("bloodmagic")
			i.click(ncon.BMX, ncon.BMY[3])

			if (start + 85) < time.time():
				feature.wandoos(True)
			else:
				feature.wandoos(False)
			if not half_energy_WANDOOS and (start + 100) < time.time():
				idle_color = i.get_pixel_color(426, 250) #100% = 525, 50% = 426, 25% = 393
				if idle_color == "59CF81":
					#print("wandos is at 25%, enabling NGU")
					half_energy_WANDOOS = True
			elif half_energy_WANDOOS:
				feature.assign_ngu(1e9, [1])
				
			if not Blood_Assigned and (start + 85) < time.time():
				nav.spells()
				i.click(ncon.BM_AUTO_NUMBERX, ncon.BM_AUTO_NUMBERY)
				time.sleep(5)
				i.click(700,310)
				i.click(ncon.BM_AUTO_NUMBERX, ncon.BM_AUTO_NUMBERY)
				Blood_Assigned = True

		
		#feature.NOV_boost_equipment("accessory5")
		feature.NOV_boost_equipment("cube")
		#feature.boost_equipment() #boostar också Cube
	
	
	if counter != 0:
		nav.menu("augmentations")
		i.click(10, 10)
		aaa = i.get_bitmap()
		aaa.save("Pic\\debug\\augment" + str(counter) + ".png")

		nav.menu("bloodmagic")
		i.click(10, 10)
		aaa = i.get_bitmap()
		aaa.save("Pic\\debug\\blood" + str(counter) + ".png")
		
		nav.menu("wandoos")
		i.click(10, 10)
		aaa = i.get_bitmap()
		aaa.save("Pic\\debug\\wandoos" + str(counter) + ".png")
	
	#nav.reclaim_all_magic()
	#nav.reclaim_all_energy()
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





w = Window(debug=True)
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 10, 10, 400, 600)
nav.menu("inventory")
u = Upgrade(37500, 37500, 2.3, 2.4, 10) #Hur den ska spendare EXP inom Energy & Magic caps
print(w.x, w.y)
print(str(w.id))
tracker = Tracker(5)		#Progress tracker int val = tid för run


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
	
	
	#kolla ifall den cappar blood magic annars öka tiden så det gör det
	#Kolla ifall jag har för mkt guld
	
	
	Nov_SpeedRun_Two(5, runCounter)
	print(str(w.id))
	print(str(Window.id))
	'''
	if runCounter % 10 == 0:
		u.em()
		tracker.adjustxp()
	'''
	runCounter += 1