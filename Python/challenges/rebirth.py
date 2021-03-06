"""Contains functions for running a no rebirth challenge."""
from classes.features import Features
import ngucon as ncon
import usersettings as userset
import time


class Rebirth(Features):
	"""Contains functions for running a no rebirth challenge."""


	LOWEST_SLEEP_TO_KILL = 3.4
	ADVENTURE_ZONE = {0: {"name": "Cave of Many Things", "boss": 37, "floor": 4, "sleep": LOWEST_SLEEP_TO_KILL},
					  1: {"name": "The Sky", "boss": 48, "floor": 5, "sleep": LOWEST_SLEEP_TO_KILL},
					  2: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
					  3: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
					  4: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
					  5: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
					  6: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": LOWEST_SLEEP_TO_KILL},
					  7: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": LOWEST_SLEEP_TO_KILL},
					  8: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": LOWEST_SLEEP_TO_KILL},
					  9: {"name": "Badly Drawn World", "boss": 116, "floor": 18, "sleep": 9},
					  10: {"name": "Boring-Ass Earth", "boss": 124, "floor": 19, "sleep": 9}}
	MAX_KILL_ADVENTURE_ZONE = 8 #if you only want to kill up towards "Mega Lands" enter 5 and it will avoid Beardverse and onwards

	def intTryParse(value):
		try:
			return int(value)
		except ValueError:
			return 0
	
	def kill_bosses(self, currentBoss, timeSinceStart, GoldClearLevels):
		room = 0
		newBossToKill = False

		for i in range(Rebirth.MAX_KILL_ADVENTURE_ZONE,-1,-1):
			if GoldClearLevels >= i:
				break
			if currentBoss > Rebirth.ADVENTURE_ZONE[i]["boss"]:
				highestBoss = currentBoss <= Rebirth.ADVENTURE_ZONE[i + 1]["boss"] #Could be better with <= but then there is a rare bug where the game has killed one more boss since the last CurrentBoss was grabbed
				
				self.reclaim_all_energy()
				self.reclaim_all_magic()
				self.loadout(1)  # Gold drop equipment
				if timeSinceStart >= 100: #before 100sec the game does not have the ability to manually attack
					self.snipe(Rebirth.ADVENTURE_ZONE[i]["floor"], 999, once=True, highest=highestBoss, bosses=True)
				else:
					self.adventure(zone=Rebirth.ADVENTURE_ZONE[i]["floor"], highest=highestBoss)
					time.sleep(Rebirth.ADVENTURE_ZONE[i]["sleep"])
				self.loadout(2)  # Bar/power equimpent

				return True, i
		return False, 0
	
	
	
	
	def first_rebirth(self):
		"""Procedure for first rebirth."""
		start = time.time()
		ThreeMinMark = time.time() + 180
		TM_assigned = False
		augment_assigned = 0
		GoldClearLevels = -1
		Wandoos_Done = False

		self.nuke(25)
		#time.sleep(1)
		self.loadout(1)
		self.adventure(highest=True)
		self.augments({"SM": 1}, 10e6)

		while True:
			if time.time() > ThreeMinMark and (not self.check_challenge()):
				self.menu("augmentations")
				self.click(10, 10)
				aaa = self.get_bitmap()
				aaa.save("Pic\\chall7_" + str(int(time.time())) + ".png")
				return

			self.nuke()
			self.fight()
			currentBoss = Rebirth.intTryParse(self.get_current_boss())
			
			var1, var2 = self.kill_bosses(currentBoss, 0, GoldClearLevels)
			if var1:
				self.adventure(itopod=True, itopodauto=True)
				GoldClearLevels = var2

				TM_assigned = False
				augment_assigned = 0
				Wandoos_Done = False

			if currentBoss > 30 and not TM_assigned:
				self.reclaim_all_energy()
				self.reclaim_all_magic()
				self.time_machine(100e6, magic=True)
				self.loadout(2)
				if (time.time() - start) < 30:
					self.augments({"EB": 1}, 10e6)
				TM_assigned = True


			if currentBoss > 48 and augment_assigned < 5:
				self.menu("augmentations")
				self.input_box()
				self.NOV_send_text(1e12)
				self.click(575, 260 + 70 * 0)#SS
				self.click(575, 290 + 70 * 0)#DS
				self.click(575, 260 + 70 * 1)#MI
				self.click(575, 290 + 70 * 1)#DTMT
				self.click(575, 260 + 70 * 2)#CI
				self.click(575, 290 + 70 * 2)#ML
				self.click(575, 260 + 70 * 3)#SM
				self.click(575, 290 + 70 * 3)#AA
				
				self.augments({"EB": 1}, 2.5e9)
				self.augments({"CS": 1}, 500e6)
				augment_assigned = 5
			elif currentBoss > 46 and augment_assigned < 4:
				self.menu("augmentations")
				self.input_box()
				self.NOV_send_text(1e12)
				self.click(575, 260 + 70 * 0)#SS
				self.click(575, 290 + 70 * 0)#DS
				self.click(575, 260 + 70 * 1)#MI
				self.click(575, 290 + 70 * 1)#DTMT
				self.click(575, 260 + 70 * 2)#CI
				self.click(575, 290 + 70 * 2)#ML
				
				self.augments({"SM": 1}, 400e6)
				self.augments({"AA": 1}, 140e6)
				augment_assigned = 4
			elif currentBoss > 44 and augment_assigned < 3:
				self.menu("augmentations")
				self.input_box()
				self.NOV_send_text(1e12)
				self.click(575, 260 + 70 * 0)#SS
				self.click(575, 290 + 70 * 0)#DS
				self.click(575, 260 + 70 * 1)#MI
				self.click(575, 290 + 70 * 1)#DTMT
				
				self.augments({"CI": 1}, 80e6)
				self.augments({"ML": 1}, 40e6)
				augment_assigned = 3
			elif currentBoss > 40 and augment_assigned < 2:
				self.menu("augmentations")
				self.input_box()
				self.NOV_send_text(1e12)
				self.click(575, 260 + 70 * 0)#SS
				self.click(575, 290 + 70 * 0)#DS
				
				self.augments({"MI": 1}, 5e6)
				self.augments({"DTMT": 1}, 5e6)
				augment_assigned = 2
			elif currentBoss > 37 and augment_assigned < 1:
				self.augments({"SS": 1}, 5e6)
				self.augments({"DS": 1}, 5e6)
				augment_assigned = 1


			self.wandoos(True)


			if TM_assigned:
				self.gold_diggers([2, 3, 8])

			if currentBoss > 37:
				self.blood_magic(6)			
			
			if not Wandoos_Done:
				self.menu("wandoos")
				#self.click(10, 10)
				idle_color = self.get_pixel_color(525, 250) #100% = 525, 50% = 426, 25% = 393
				idle_color2 = self.get_pixel_color(525, 350)
				
				if idle_color == "59CF81" and idle_color2 == "A9BAF9":
					Wandoos_Done = True
			
			if Wandoos_Done:
				self.time_machine(1e12, magic=True)


	def check_challenge(self):
		"""Check if a challenge is active."""
		self.rebirth()
		self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
		time.sleep(userset.LONG_SLEEP)
		color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
									 ncon.CHALLENGEACTIVEY)

		return True if color == ncon.CHALLENGEACTIVECOLOR else False

	def rebirth_challenge(self):
		"""Defeat target boss."""
		self.first_rebirth()
