"""Contains functions for running a basic challenge."""
from classes.features import Features
import ngucon as ncon
import usersettings as userset
import time


class Basic(Features):
	"""Contains functions for running a basic challenge."""

	def first_rebirth(self, duration, counter):
		"""Procedure for first rebirth after number reset."""
		start = time.time()
		end = time.time() + (duration * 60)
		augemnt_assigned = 0
		currentBoss = 0
		GoldClearLevels = 0 #1=Sewers,2=Forest
		TM_assigned = False

		self.loadout(1)
		
		while time.time() < (end - 2):
			self.nuke()
			time.sleep(0.5)
			self.fight()
			
			try:
				currentBoss = int(self.get_current_boss())
			except:
				print("Failed to get boss level")
			
			if (GoldClearLevels == 0 and currentBoss > 7) or (GoldClearLevels == 1 and currentBoss > 17):
				self.adventure(highest=True)
				GoldClearLevels += 1
			if currentBoss > 17 and augemnt_assigned == 0:
				self.menu("augmentations")
				self.click(630, 260 + 70 * 0)
				self.send_string(2)
				self.click(630, 260 + 70 * 1)
				self.send_string(2)
				
				self.augments({"SS": 1}, 1e3)
				augemnt_assigned += 1
			elif currentBoss > 18 and augemnt_assigned == 1:
				self.augments({"MI": 1}, 1e4)
				augemnt_assigned += 1
			elif currentBoss > 20 and augemnt_assigned == 2:
				self.augments({"CI": 1}, 1e4)
				augemnt_assigned += 1
				
			if currentBoss > 30 and not TM_assigned:
				self.reclaim_all_energy()
				self.time_machine(5e6, magic=True)
				self.augments({"EB": 1}, 40e6)
				TM_assigned = True
				
			self.wandoos(True)
		
		self.menu("augmentations")
		self.click(630, 260 + 70 * 0)
		self.send_string(0)
		self.click(630, 260 + 70 * 1)
		self.send_string(0)
		
		self.rebirth()
		self.click(10, 10)
		aaa = self.get_bitmap()
		aaa.save("Pic\\" + "challenge" + str(counter) + ".png")
		
		while time.time() < end:
			time.sleep(0.1)

	def speedrun(self, duration, counter):
		#Start a speedrun.
		
		self.do_rebirth()
		start = time.time()
		end = time.time() + (duration * 60) + 1
		currentBoss = 0
		GoldClearLevels = 1 #1=Sewers,2=Forest
		TM_assigned = 0
		augemnt_assigned = -1
		blood_assigned = False
		digger_activated = False
		
		self.nuke()
		time.sleep(2)
		self.loadout(1)
		
		while time.time() < (end - 10) and currentBoss <= 58:
			self.nuke()
			time.sleep(0.5)
			self.fight()			
			try:
				currentBoss = int(self.get_current_boss())
			except:
				print("Failed to get boss level")

			if currentBoss > 30 and TM_assigned <= 3:
				if TM_assigned == 0:
					self.loadout(2)
					self.reclaim_all_energy()
					self.reclaim_all_magic()
				self.time_machine(1e9, magic=True)
				TM_assigned += 1
			
			if (GoldClearLevels == 1 and currentBoss > 17) or (GoldClearLevels == 2 and currentBoss > 37) \
										or (GoldClearLevels == 3 and currentBoss > 48):
				if GoldClearLevels >= 2:
					self.loadout(1)
					self.adventure(highest=True)
					time.sleep(8)
					self.loadout(2)  # Bar/power equimpent
					self.adventure(itopod=True, itopodauto=True)
				else:
					self.adventure(highest=True)
				GoldClearLevels += 1
			
			
			if currentBoss > 37 and augemnt_assigned != 2:
				self.menu("augmentations")
				time.sleep(5)
				#print("Augment 2")
				self.click(575, 390)
				self.click(575, 525)
				self.augments({"SS": 0.95, "DS": 0.5}, 5e6)
				augemnt_assigned = 2
			elif currentBoss > 31 and augemnt_assigned < 1:
				self.menu("augmentations")
				time.sleep(5)
				#print("Augment 1")
				self.click(575, 390)
				self.augments({"EB": 1}, 20e6)
				augemnt_assigned = 1
			elif augemnt_assigned == -1:
				self.menu("augmentations")
				time.sleep(5)
				#print("Augment 0")
				self.augments({"CI": 1}, 20e6)
				augemnt_assigned = 0

			if currentBoss > 37 and not blood_assigned:
				self.menu("wandoos")
				self.click(590, 350)
				self.blood_magic(3)
				blood_assigned = True
			
			if currentBoss > 35 and not digger_activated \
				and time.time() > (start + 80):
				#print("digger on")
				self.gold_diggers([2], True)
				digger_activated = True
				
			self.gold_diggers([2])
			self.wandoos(True)
			time.sleep(3)
		
		if currentBoss >= 59:
			#print("Already done :)")
			while (time.time() - start) <= 180:
				time.sleep(0.25)
		else:
			self.reclaim_all_magic()
			self.reclaim_all_energy()
			if digger_activated:
				self.gold_diggers([2], activate=True)
			self.gold_diggers([3], activate=True)
			for x in range(5):
				self.nuke()
				self.fight()
				time.sleep(0.5)
			
			'''
			self.rebirth()
			self.click(10, 10)
			aaa = self.get_bitmap()
			aaa.save("Pic\\" + "challenge" + str(counter) + ".png")
			'''
			
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
	
	def basic(self, target):
		"""Defeat target boss."""
		
		#spend all exp
		#spend all perk points
		#set augment to 0 in everything
		
		self.first_rebirth(5, 1)
		self.do_rebirth()
		self.first_rebirth(5, 2)
		#self.do_rebirth()
		#self.first_rebirth(5, 3)

		abc = 3
		for x in range(8):
			self.speedrun(5, abc)
			abc += 1
			if not self.check_challenge():
				return