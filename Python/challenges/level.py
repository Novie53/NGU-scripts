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
		Blood_assigned = False

		
		self.menu("beard")
		self.click(450, 230)#Disable all beards
		if phase == 1:
			self.click(313, 319)#Select Beard 1
			self.click(316, 234)#Activate selected beard

		self.loadout(1)
		
		while time.time() < (end - 5):
			self.nuke()
			self.fight()
			currentBoss = Level.intTryParse(self.get_current_boss())

			if (GoldClearLevels == 0 and currentBoss > 7) or (GoldClearLevels == 1 and currentBoss > 17) \
				or (GoldClearLevels == 2 and currentBoss > 37) or (GoldClearLevels == 3 and currentBoss > 48):
				self.adventure(highest=True)
				GoldClearLevels += 1

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

			if currentBoss > 30 and not TM_assigned:
				self.menu("timemachine")
				self.click(685, 235)#Energy
				self.NOV_send_text(40)
				self.click(685, 335)#Magic
				self.NOV_send_text(40)
				self.click(10, 10)#defocus magic textbox
				
				if phase < 2:
					self.reclaim_all_energy()
					self.reclaim_all_magic()
				
				self.time_machine(1e9, magic=True)
				TM_assigned = True
				
				#time.sleep(2)
				#self.NOV_gold_diggers([3], [1], True)
				
				if phase < 2:
					self.click(630, 260 + 70 * 4)#EB
					self.NOV_send_text(0)
					self.augments({"EB": 1}, 10e6)

			#if TM_assigned:
			#	self.gold_diggers([3])

			if phase < 2:
				self.assign_ngu(1e9, [1])
				self.assign_ngu(1e9, [1], magic=True)

			if currentBoss > 37 and not Blood_assigned:
				self.reclaim_all_magic()
				self.menu("bloodmagic")
				self.click(ncon.BMX, ncon.BMY[3])
				Blood_assigned = True

		#self.reclaim_all_magic()
		#self.reclaim_all_energy()
		
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
		aaa.save("Pic\\rebirth" + str(counter) + ".png")
		
	def lc(self):
		"""Handle LC run."""
		
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
