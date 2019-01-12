"""Contains functions for running a no rebirth challenge."""
from classes.features import Features
import ngucon as ncon
import usersettings as userset
import time


class Rebirth(Features):
	"""Contains functions for running a no rebirth challenge."""


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
	
	def kill_bosses(self, currentBoss, timeSinceStart, GoldClearLevels):
		room = 0
		newBossToKill = False

		for i in range(Rebirth.MAX_KILL_ADVENTURE_ZONE,-1,-1):
			if GoldClearLevels >= i:
				break
			if currentBoss > Rebirth.ADVENTURE_ZONE[i]["boss"]:
				highestBoss = currentBoss <= Rebirth.ADVENTURE_ZONE[i + 1]["boss"] #Could be better with <= but then there is a rare bug where the game has killed one more boss since the last CurrentBoss was grabbed
				
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
		end = time.time() + 3 * 60
		TM_assigned = False
		bm_unlocked = False
		ci_assigned = False
		diggers = [2, 3, 8]
		GoldClearLevels = -1

		self.nuke()
		time.sleep(1)		
		self.loadout(1)
		self.adventure(highest=True)

		while True:
			self.nuke()
			self.fight()
			currentBoss = Rebirth.intTryParse(self.get_current_boss())
			
			if currentBoss > 37:
				var1, var2 = self.kill_bosses(currentBoss, 0, GoldClearLevels)
				if var1:
					self.adventure(itopod=True, itopodauto=True)
					GoldClearLevels = var2
		
			self.wandoos(True)
			if not ci_assigned:
				self.augments({"CI": 1}, 1e6)
				ci_assigned = True
		
			if currentBoss > 30 and not TM_assigned:
				self.reclaim_all_energy()
				self.reclaim_all_magic()
				self.time_machine(10e6, magic=True)
				self.loadout(2)
				self.augments({"EB": 1}, 80e6)
				TM_assigned = True
				
			if TM_assigned:
				self.gold_diggers([2, 3])
				
			if not self.check_challenge() and time.time() > end:
				return

		'''
		while not bm_unlocked:
			self.wandoos(True)
			self.nuke()
			time.sleep(2)
			self.fight()
			self.gold_diggers(diggers)
			time.sleep(5)

			bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
			if bm_color != ncon.BMLOCKEDCOLOR:
				self.menu("bloodmagic")
				time.sleep(0.2)
				self.blood_magic(8)
				bm_unlocked = True
				self.augments({"SS": 0.7, "DS": 0.3}, 5e8)
		final_aug = False
		while True:
			self.wandoos(True)
			self.nuke()
			time.sleep(2)
			try:
				current_boss = int(self.get_current_boss())
				if current_boss > 56 and not final_aug:
					self.augments({"AE": 0.7, "ES": 0.3}, 1e11)
					final_aug = True
			except ValueError:
				print("couldn't get current boss")
			self.fight()
			self.gold_diggers(diggers)
			time.sleep(10)

			if not self.check_challenge() and time.time() > end:
				return
		'''

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
		return
