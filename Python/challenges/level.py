"""Contains functions for running a 100 level challenge."""
from classes.features import Features
import ngucon as ncon
import time


class Level(Features):
	"""Contains functions for running a 100 level challenge.

	IMPORTANT

	If you're reusing this code - make sure to check the augments used in the
	first_lc() and speedrun_lc() functions can be used by you as well, or
	if you can use a higher augment for higher speed. Also make sure to put a
	target level on all used augments and time machine, as well as disabling
	all beards before running.
	"""

	def intTryParse(value):
		try:
			return int(value)
		except ValueError:
			return 0
	
	
	
	
	def first_rebirth(self, duration, phase = 1):
		"""Procedure for first rebirth after number reset."""
		start = time.time()
		end = time.time() + (duration * 60)
		augment_assigned = 0
		currentBoss = 0
		GoldClearLevels = 0 #1=Sewers,2=Forest
		TM_assigned = False

		
		if phase == 1:
			self.menu("beard")
			self.click(450, 230)#Disable all beards
			self.click(313, 319)#Select Beard 1
			self.click(316, 234)#Activate selected beard
		self.loadout(1)
		
		while time.time() < (end - 2):
			self.nuke()
			self.fight()
			currentBoss = Level.intTryParse(self.get_current_boss())


			if GoldClearLevels < 3 and currentBoss > 37:
				self.loadout(1)
				self.adventure(highest=True)
				time.sleep(4)
				self.loadout(2)
				GoldClearLevels = 3
			if (GoldClearLevels == 0 and currentBoss > 7) or (GoldClearLevels == 1 and currentBoss > 17):
				self.adventure(highest=True)
				GoldClearLevels += 1

			if phase == 1:
				if currentBoss > 17 and augment_assigned <= 0:
					self.menu("augmentations")
					self.click(630, 260 + 70 * 0)#SS
					self.NOV_send_text(1)
					self.click(630, 260 + 70 * 1)#MI
					self.NOV_send_text(1)
					self.click(630, 260 + 70 * 2)#CI
					self.NOV_send_text(2)
					self.click(630, 260 + 70 * 3)#SM
					self.NOV_send_text(3)

					self.augments({"SS": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 18 and augment_assigned <= 1:
					self.augments({"MI": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 20 and augment_assigned <= 2:
					self.augments({"CI": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 24 and augment_assigned <= 3:
					self.augments({"SM": 1}, 1e6)
					augment_assigned += 1
			elif phase == 2:
				if currentBoss > 24 and augment_assigned == 0:
					self.click(630, 260 + 70 * 3)#SM
					self.NOV_send_text(1)
					self.click(630, 260 + 70 * 4)#EB
					self.NOV_send_text(40)

					self.augments({"SM": 1}, 1e6)
					augment_assigned += 1
				elif currentBoss > 28 and augment_assigned == 1:
					self.augments({"EB": 1}, 40e6)
					augment_assigned += 1

			if currentBoss > 30 and not TM_assigned:
				self.menu("timemachine")
				self.click(685, 235)#Energy
				self.NOV_send_text(15)
				self.click(685, 335)#Magic
				self.NOV_send_text(15)
				self.click(10, 10)#defocus magic textbox
				
				if phase == 1:
					self.reclaim_all_energy()
				
				
				self.time_machine(1e9, magic=True)
				self.loadout(2)
				
#				time.sleep(5)
#				self.gold_diggers([3], True)
				TM_assigned = True

#			if TM_assigned:
#				self.gold_diggers([3])

			if phase == 1:
				self.assign_ngu(1e9, [1])
				self.assign_ngu(1e9, [1], magic=True)


		self.reclaim_all_magic()
		self.reclaim_all_energy()
		
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
			time.sleep(1)
			self.nuke()
			self.fight()
			time.sleep(1)
		
		
		while time.time() < end:
			time.sleep(0.1)

	def lc_speedrun(self):
		"""Procedure for first rebirth in a 100LC."""
		self.do_rebirth()
		start = time.time()
		end = time.time() + 3 * 60
		tm_unlocked = False
		
		self.fight()
		self.adventure(highest=True)
		try:
			current_boss = int(self.get_current_boss())
		except ValueError:
			print("error reading current boss")
			current_boss = 1

		while current_boss < 25:
			self.fight()
			time.sleep(5)
			try:
				current_boss = int(self.get_current_boss())
			except ValueError:
				print("error reading current boss")
				current_boss = 1
				if time.time() > start + 60:
					current_boss = 25

		if current_boss < 29:  # EB not unlocked
			self.augments({"SM": 1}, 1e8)

		while not tm_unlocked:
			self.fight()

			tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
			if tm_color != ncon.TMLOCKEDCOLOR:
				self.time_machine(True)
				tm_unlocked = True

		time.sleep(5)
		for x in range(5):  # it doesn't add energy properly sometimes.
			self.augments({"EB": 1}, 1e8)

		self.gold_diggers([3], True)
		time.sleep(4)

		while current_boss < 38:
			self.fight()
			time.sleep(5)
			try:
				current_boss = int(self.get_current_boss())
			except ValueError:
				print("error reading current boss")
				current_boss = 1
				if time.time() > start + 180:
					current_boss = 25

		self.menu("bloodmagic")
		time.sleep(0.2)
		self.click(ncon.BMX, ncon.BMY[3])

		while time.time() < end + 3:
			self.fight()
			self.gold_diggers([3])
			self.adventure(highest=True)
			time.sleep(5)

		return

	def check_challenge(self):
		"""Check if a challenge is active."""
		self.rebirth()
		self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
		time.sleep(ncon.LONG_SLEEP)
		color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
									 ncon.CHALLENGEACTIVEY)

		return True if color == ncon.CHALLENGEACTIVECOLOR else False

	def lc(self):
		"""Handle LC run."""
		self.first_rebirth(3)
		print("1 done")
		self.do_rebirth()
		self.first_rebirth(3)
		print("2 done")
		self.do_rebirth()
		self.first_rebirth(3)
		print("3 done, starting p2")
		self.do_rebirth()
		self.first_rebirth(3, phase = 2)
		print("4 done")
		input("input waiting")
		self.do_rebirth()
		self.first_rebirth(3, phase = 2)
		print("5 done")
		self.do_rebirth()
		self.first_rebirth(3, phase = 2)
		print("6 done")
		
		#Todo try two 5 min runs instead
		while True:
			self.lc_speedrun()
			if not self.check_challenge():
				return
