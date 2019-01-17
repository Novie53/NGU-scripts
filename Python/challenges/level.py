"""Contains functions for running a 100 level challenge."""
from classes.features import Features
import ngucon as ncon
import time
import usersettings as userset


class Level(Features):
	"""Contains functions for running a 100 level challenge.

	IMPORTANT

	If you're reusing this code - make sure to check the augments used in the
	first_lc() and speedrun_lc() functions can be used by you as well, or
	if you can use a higher augment for higher speed. Also make sure to put a
	target level on all used augments and time machine, as well as disabling
	all beards before running.
	"""
	LOWEST_SLEEP_TO_KILL = 3.7
	ADVENTURE_ZONE = {0: {"name": "Cave of Many Things", "boss": 37, "floor": 4, "sleep": LOWEST_SLEEP_TO_KILL},
					  1: {"name": "The Sky", "boss": 48, "floor": 5, "sleep": LOWEST_SLEEP_TO_KILL},
					  2: {"name": "High Security Base", "boss": 58, "floor": 6, "sleep": LOWEST_SLEEP_TO_KILL},
					  3: {"name": "Clock Dimension", "boss": 66, "floor": 8, "sleep": LOWEST_SLEEP_TO_KILL},
					  4: {"name": "The 2D Universe", "boss": 74, "floor": 10, "sleep": LOWEST_SLEEP_TO_KILL},
					  5: {"name": "Ancient Battlefield", "boss": 82, "floor": 11, "sleep": LOWEST_SLEEP_TO_KILL},
					  6: {"name": "A Very Strange Place", "boss": 90, "floor": 13, "sleep": LOWEST_SLEEP_TO_KILL},
					  7: {"name": "Mega Lands", "boss": 100, "floor": 14, "sleep": 8},
					  8: {"name": "The Beardverse", "boss": 108, "floor": 16, "sleep": 9}}
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




	def first_rebirth(self, duration, phase = 1):
		"""Procedure for first rebirth after number reset."""
		start = time.time()
		end = time.time() + (duration * 60)
		augment_assigned = 0
		currentBoss = 0
		GoldClearLevels = 0 #1=Sewers,2=Forest
		TM_assigned = False
		Blood_assigned = False


		self.nuke()
		time.sleep(1)
		self.loadout(1)
		self.adventure(highest=True)
		
		while time.time() < (end - 5):
			self.nuke()
			self.fight()
			currentBoss = Level.intTryParse(self.get_current_boss())

			if currentBoss > 37:
				var1, var2 = Level.kill_bosses(currentBoss, 0, GoldClearLevels)
				if var1:
					#self.adventure(itopod=True, itopodauto=True)
					GoldClearLevels = var2

			if currentBoss > 30 and not TM_assigned:
				self.menu("timemachine")
				self.click(685, 235)#Energy
				self.NOV_send_text(35)
				self.click(685, 335)#Magic
				self.NOV_send_text(35)
				self.click(10, 10)#defocus magic textbox
				
				self.reclaim_all_energy()
				self.reclaim_all_magic()
				
				self.loadout(2)
				
				self.time_machine(1e12, magic=True)
				TM_assigned = True

			if TM_assigned:
				self.gold_diggers([3])

			if currentBoss > 24 and augment_assigned == 0:
				self.menu("augmentations")
				self.click(630, 260 + 70 * 3)#SM
				self.NOV_send_text(2)
				self.click(630, 260 + 70 * 4)#EB
				self.NOV_send_text(8)
				
				self.augments({"SM": 1}, 100e6)
				augment_assigned += 1
			elif TM_assigned and augment_assigned == 1:
				self.augments({"EB": 1}, 100e6)
				augment_assigned += 1
			"""
			if phase < 2:
				if currentBoss > 17 and augment_assigned <= 0:
					self.menu("augmentations")
					self.click(630, 260 + 70 * 0)#SS
					self.NOV_send_text(-1)
					self.click(630, 260 + 70 * 1)#MI
					self.NOV_send_text(1)
					self.click(630, 260 + 70 * 2)#CI
					self.NOV_send_text(2)
					self.click(630, 260 + 70 * 3)#SM
					self.NOV_send_text(3)
					self.click(630, 260 + 70 * 4)#EB
					self.NOV_send_text(10)

					self.augments({"SS": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 18 and augment_assigned <= 1:
					self.augments({"MI": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 20 and augment_assigned <= 2:
					self.augments({"CI": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 24 and augment_assigned <= 3:
					self.augments({"SM": 1}, 10e6)
					augment_assigned += 1
				elif currentBoss > 28 and augment_assigned <= 4:
					self.augments({"EB": 1}, 10e6)
					augment_assigned += 1
			elif phase == 2:
				if currentBoss > 24 and augment_assigned == 0:
					self.menu("augmentations")
					self.click(630, 260 + 70 * 3)#SM
					self.NOV_send_text(1)
					self.click(630, 260 + 70 * 4)#EB
					self.NOV_send_text(10)

					self.augments({"SM": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 28 and augment_assigned == 1:
					self.augments({"EB": 1}, 40e6)
					augment_assigned += 1
			"""


			"""
			if currentBoss > 37 and not Blood_assigned:
				self.reclaim_all_magic()
				self.menu("bloodmagic")
				self.click(ncon.BMX, ncon.BMY[3])
				Blood_assigned = True
			"""

		#self.reclaim_all_magic()
		#self.reclaim_all_energy()
		
		self.menu("augmentations")
		#self.click(630, 260 + 70 * 0)#SS
		#self.NOV_send_text(-1)
		#self.click(630, 260 + 70 * 1)#MI
		#self.NOV_send_text(-1)
		#self.click(630, 260 + 70 * 2)#CI
		#self.NOV_send_text(-1)
		self.click(630, 260 + 70 * 3)#SM
		self.NOV_send_text(-1)
		self.click(630, 260 + 70 * 4)#EB
		self.NOV_send_text(-1)
		
		if TM_assigned:
			self.menu("timemachine")
			self.click(685, 235)#Energy
			self.NOV_send_text(0)
			self.click(685, 335)#Magic
			self.NOV_send_text(0)	
		
		self.menu("beard")
		self.click(450, 230)#Disable all beards
		
		if phase == 1:
			self.wandoos(True)
		else:
			self.gold_diggers([3], True)

		self.nuke()
		time.sleep(0.5)
		for i in range(5):
			self.fight()
			time.sleep(0.5)

		while time.time() < end:
			time.sleep(0.1)

	def check_challenge(self):
		"""Check if a challenge is active."""
		self.rebirth()
		self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
		time.sleep(userset.LONG_SLEEP)
		color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
									 ncon.CHALLENGEACTIVEY)

		return True if color == ncon.CHALLENGEACTIVECOLOR else False

	def printScreen(self, counter):
		self.rebirth()
		self.click(10, 10)
		aaa = self.get_bitmap()
		aaa.save("Pic\\chall4_" + str(counter) + ".png")
		
	def lc(self):
		"""Handle LC run."""
		
		"""
			Disabla bears
			sätt -1 i alla augments
			wandoos MEH
			stäng av blood auto gold
		
		"""
		"""
		self.menu("beard")
		self.click(450, 230)#Disable all beards
		
		self.menu("augmentations")
		self.click(630, 260 + 70 * 0)#SS
		self.NOV_send_text(-1)
		self.click(630, 260 + 70 * 1)#MI
		self.NOV_send_text(-1)
		self.click(630, 260 + 70 * 2)#CI
		self.NOV_send_text(-1)
		self.click(630, 260 + 70 * 3)#SM
		self.NOV_send_text(-1)
		self.click(630, 260 + 70 * 4)#EB
		self.NOV_send_text(-1)
		"""		
		
		self.first_rebirth(3)
		self.printScreen(1)
		
		self.do_rebirth()
		self.first_rebirth(3, phase = 1.25)
		self.printScreen(2)
		
		self.do_rebirth()
		self.first_rebirth(3)
		self.printScreen(3)
		
		counter = 4
		while True:
			self.do_rebirth()
			self.first_rebirth(3, phase = 2)
			self.printScreen(counter)
			counter += 1
			if not self.check_challenge():
				return
