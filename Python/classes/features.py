"""Feature class handles the different features in the game."""
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
from collections import deque, namedtuple
from decimal import Decimal
import math
import ngucon as ncon
import re
import time
import win32con as wcon
import win32gui
import usersettings as userset
import datetime
import re


class Features(Navigation, Inputs):
	"""Handles the different features in the game."""

#------------ Fight Boss ---------------
	'''
	def get_current_boss(self):
		"""Go to fight and read current boss number."""
		self.menu("fight")
		boss = self.ocr(ncon.OCRBOSSX1, ncon.OCRBOSSY1, ncon.OCRBOSSX2,
						ncon.OCRBOSSY2, debug=False)
		return self.remove_letters(boss)
	'''
	
	def get_current_boss_two(self):
		"""Go to fight and read current boss number."""
		self.menu("fight")
		boss = self.ocr(ncon.OCRBOSSX1, ncon.OCRBOSSY1, ncon.OCRBOSSX2,
						ncon.OCRBOSSY2, debug=False)
		boss = self.remove_letters(boss)
		try:
			return int(boss)
		except ValueError:
			print("get_current_boss_two failed")
			return -1

	def nuke(self, boss=None):
		"""Navigate to Fight Boss and Nuke or Fast Fight."""
		self.menu("fight")
		if boss:
			for i in range(boss):
				self.click(ncon.FIGHT_BOSS_X, ncon.FIGHT_Y, fast=0.05)
			time.sleep(userset.SHORT_SLEEP)
			current_boss = self.get_current_boss_two()
			x = 0
			while current_boss < boss:
				bossdiff = boss - current_boss
				for i in range(0, bossdiff):
					self.click(ncon.FIGHT_BOSS_X, ncon.FIGHT_Y, fast=True)
				time.sleep(userset.SHORT_SLEEP)
				current_boss = self.get_current_boss_two()
				x += 1
				if x > 7:  # Safeguard if number is too low to reach target boss, otherwise we get stuck here
					print("Couldn't reach the target boss, something probably went wrong the last rebirth.")
					break
		else:
			self.click(ncon.FIGHT_BOSS_X, ncon.NUKE_Y)
			time.sleep(userset.MEDIUM_SLEEP)

	def fight(self):
		"""Navigate to Fight Boss and click fight."""
		self.menu("fight")
		self.click(ncon.FIGHT_BOSS_X, ncon.FIGHT_Y)

	def stop_fight(self):
		self.menu("fight")
		self.click(ncon.FIGHT_BOSS_X, ncon.STOP_Y)

#------------ Money Pit ----------------
	def spin(self):
		"""Spin the wheel."""
		self.menu("pit")
		self.click(ncon.SPIN_MENUX, ncon.SPIN_MENUY)
		self.click(ncon.SPINX, ncon.SPINY)

	def pit(self, loadout=0, value=0):
		"""Throws money into the pit.
		Keyword arguments:
		loadout -- The loadout you wish to equip before throwing gold
				   into the pit, for gear you wish to shock. Make
				   sure that you don't get cap-blocked by either using
				   the unassign setting in the game or swapping gear that
				   doesn't have e/m cap.
		"""		
		def _ocr():
			try:
				return float((self.ocr(15, 320, 140, 350)).replace(" ",""))
			except:
				print("Money Pit OCR Failed")
				return 1e99
			
		color = self.get_pixel_color(ncon.PITCOLORX, ncon.PITCOLORY)
		if (color == ncon.PITREADY):
			self.menu("pit")

			if value != 0:
				currentMoney = _ocr()
				if currentMoney < value:
					self.reclaim_all_magic()
					self.reclaim_all_energy()
					self.deactivate_all_diggers()
					self.time_machine(1e12, magic=True)
					print("Waiting on Money Pit")
					self.menu("pit")
					while currentMoney < value:
						currentMoney = _ocr()
						time.sleep(0.25)
			if loadout:
				self.loadout(loadout)
			self.menu("pit")
			self.click(ncon.PITX, ncon.PITY)
			self.click(ncon.CONFIRMX, ncon.CONFIRMY)
			if loadout:
				self.loadout(2)


#------------ Adventure ----------------
#Sub Adv Functions
	def _Is_Mob_Alive(self):
		self.menu("adventure")
	
		health = self.get_pixel_color(706, 302) #if the "POWER:{DMG}" text is displayed"
		healthRowTwo = self.get_pixel_color(706, 318) #if the "POWER:{DMG}" text is displayed". 
		#In the case of mobs with names that are two lines long the Max HP info shifts
		return health == "000000" or healthRowTwo == "000000"

	def _Lick_Wounds(self):
		self.menu("adventure")
	
		my_health = self.get_pixel_color(ncon.PLAYER_HEAL_THRESHOLDX, ncon.PLAYER_HEAL_THRESHOLDY)
		if my_health == ncon.PLAYER_HEAL_COLOR:
			print("going back to base to lick my wounds")
			self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
			while my_health == ncon.PLAYER_HEAL_COLOR:
				my_health = self.get_pixel_color(ncon.PLAYER_HEAL_THRESHOLDX + 30, ncon.PLAYER_HEAL_THRESHOLDY)
				time.sleep(0.1)
			print("done licking my wounds")
			return True
		else:
			return False

	def _Set_IdleAttack_State(self, state):
		self.menu("adventure")
	
		idle_color = self.get_pixel_color(ncon.ABILITY_ROW1X, ncon.ABILITY_ROW1Y)
		if (idle_color == ncon.IDLECOLOR and not state) or \
					(idle_color != ncon.IDLECOLOR and state):
			self.click(ncon.IDLE_BUTTONX, ncon.IDLE_BUTTONY)
			self.click(10, 10)
			time.sleep(1)

	def _Is_Boss(self):
		self.menu("adventure")
	
		crown = self.get_pixel_color(ncon.CROWNX, ncon.CROWNY)
		return crown == ncon.ISBOSS

	def _Set_BEAST_MODE_State(self, state, wait=False):
		def Is_BEAST_MODE_Ready():
			button_Color = self.get_pixel_color(ncon.ABILITY_ROW3X + ncon.ABILITY_OFFSETX * 2, ncon.ABILITY_ROW3Y)
			return button_Color == ncon.ABILITY_ROW3_READY_COLOR
	
		self.menu("adventure")
	
		start = time.time()
		border_color = self.get_pixel_color(ncon.BEAST_MODE_BORDER_X, ncon.BEAST_MODE_BORDER_Y)
		BEAST_MODE_Active = border_color == ncon.BEAST_MODE_ACTIVE_BORDER_COLOR
		if (state and not BEAST_MODE_Active) or \
			(not state and BEAST_MODE_Active):
			
			while wait and not Is_BEAST_MODE_Ready():
				if (time.time() - start) > 20:
					raise RuntimeError("BEAST MODE has waited for longed than 20 sec when it should only possibly need to wait 15 sec. SHOULD NOT HAPPEN")
				time.sleep(0.1)
			if Is_BEAST_MODE_Ready():
				self.click(ncon.ABILITY_ROW3X + ncon.ABILITY_OFFSETX * 2, ncon.ABILITY_ROW3Y)
				self.click(10, 10)
				time.sleep(1)

	def _ITOPOD_Active(self):
		self.menu("adventure")
	
		itopod_active = self.get_pixel_color(ncon.ITOPOD_ACTIVEX, ncon.ITOPOD_ACTIVEY)
		return itopod_active == "000000"

	def _Manual_Kill(self, onlyAttack=False):
		self.menu("adventure")
	
		queue = deque(self._Get_Ability_Queue(onlyAttack=onlyAttack))
		while self._Is_Mob_Alive():
			if len(queue) == 0:
				#print("NEW QUEUE")
				queue = deque(self._Get_Ability_Queue(onlyAttack=onlyAttack))

			ability = queue.popleft()
			#print(f"using ability {ability}")
			if ability <= 4:
				x = ncon.ABILITY_ROW1X + ability * ncon.ABILITY_OFFSETX
				y = ncon.ABILITY_ROW1Y

			if ability >= 5 and ability <= 10:
				x = ncon.ABILITY_ROW2X + (ability - 5) * ncon.ABILITY_OFFSETX
				y = ncon.ABILITY_ROW2Y

			if ability > 10:
				x = ncon.ABILITY_ROW3X + (ability - 11) * ncon.ABILITY_OFFSETX
				y = ncon.ABILITY_ROW3Y

			self.click(x, y)
			self.click(10, 10)
			time.sleep(userset.LONG_SLEEP)
			color = self.get_pixel_color(ncon.ABILITY_ROW1X, ncon.ABILITY_ROW1Y)

			while color != ncon.ABILITY_ROW1_READY_COLOR:
				time.sleep(0.03)
				color = self.get_pixel_color(ncon.ABILITY_ROW1X, ncon.ABILITY_ROW1Y)
		self.click(10, 10)

	def _Manual_Basic_Attack(self):
		self.menu("adventure")
	
		while self._Is_Mob_Alive():
			self.click(ncon.ABILITY_ROW1X, ncon.ABILITY_ROW1Y)
			time.sleep(0.01)

		color = self.get_pixel_color(ncon.ABILITY_ROW1X, ncon.ABILITY_ROW1Y)
		while color != ncon.ABILITY_ROW1_READY_COLOR:
			time.sleep(0.01)
			color = self.get_pixel_color(ncon.ABILITY_ROW1X, ncon.ABILITY_ROW1Y)
		self.click(10, 10)

	def _Get_Ability_Queue(self, onlyAttack=False):
		self.menu("adventure")
	
		"""Return a queue of usable abilities."""
		ready = []
		queue = []

		# Add all abilities that are ready to the ready array
		for i in range(13):
			if i <= 4:
				x = ncon.ABILITY_ROW1X + i * ncon.ABILITY_OFFSETX
				y = ncon.ABILITY_ROW1Y
				color = self.get_pixel_color(x, y)
				if color == ncon.ABILITY_ROW1_READY_COLOR:
					ready.append(i)
			if i >= 5 and i <= 10:
				x = ncon.ABILITY_ROW2X + (i - 5) * ncon.ABILITY_OFFSETX
				y = ncon.ABILITY_ROW2Y
				color = self.get_pixel_color(x, y)
				if color == ncon.ABILITY_ROW2_READY_COLOR:
					ready.append(i)
			if i > 10:
				x = ncon.ABILITY_ROW3X + (i - 11) * ncon.ABILITY_OFFSETX
				y = ncon.ABILITY_ROW3Y
				color = self.get_pixel_color(x, y)
				if color == ncon.ABILITY_ROW3_READY_COLOR:
					ready.append(i)

		health = self.get_pixel_color(ncon.PLAYER_HEAL_THRESHOLDX,
									  ncon.PLAYER_HEAL_THRESHOLDY)
		# heal if we need to heal
		if health == ncon.PLAYER_HEAL_COLOR:
			if 12 in ready:
				queue.append(12)
			elif 7 in ready:
				queue.append(7)

		# check if offensive buff and ultimate buff are both ready
		buffs = [8, 10]
		if all(i in ready for i in buffs):
			queue.extend(buffs)

		if onlyAttack:
			d = ncon.ABILITY_PRIORITY_ONLY_ATTACK
		else:
			d = ncon.ABILITY_PRIORITY

		# Sort the abilities by the set priority
		abilities = sorted(d, key=d.get, reverse=True)
		# Only add the abilities that are ready to the queue
		queue.extend([a for a in abilities if a in ready])

		# If nothing is ready, return a regular attack
		if len(queue) == 0:
			queue.append(0)

		return queue

#Main Adv Functions
	def ITOPOD_sniping(self, duration, force=False):
		self.menu("adventure")

		if not self._ITOPOD_Active() or force:
			self.click(ncon.ITOPOD_MENU_X, ncon.ITOPOD_MENU_Y)
			self.click(ncon.ITOPOD_AUTO_FLOOR_X, ncon.ITOPOD_AUTO_FLOOR_Y)
			self.click(ncon.ITOPOD_ENTER_X, ncon.ITOPOD_ENTER_Y)
		
		end = time.time() + duration
		while time.time() < end:
			self._Set_IdleAttack_State(False)
			self._Set_BEAST_MODE_State(True)
			if self._Is_Mob_Alive():
				self._Manual_Basic_Attack()
			else:
				time.sleep(0.01)
		self._Set_IdleAttack_State(True)

	def snipe_hard(self, zone, duration, once=False, highest=False, mobs=0, attackType=0, forceStay=False):
		"""
			Keyword arguments:
			zone = the zone where you want to snipe unless you set highest to True
			duration = the time spent sniping in seconds
			once = if True will end after one kill
			highest = if True will go to the highest zone
			mobs = 0=All Mobs, 1=Only bosses, 2=All execpt Bosses
			attackType = 0=All skills, 1=Only attack skills and buffs, 2=ONLY BASIC attack
			forceStay = if true will force adventure to stay in zone to save kill count for macguffin
		"""
		
		self.menu("adventure")
		self.click(10, 10)
		if attackType == 2:
			mobs = 0
		if not forceStay:
			self.adventure(zone=zone, highest=highest)
		end = time.time() + duration
		while time.time() < end:
			self._Set_IdleAttack_State(False)
			if attackType >= 1:
				self._Set_BEAST_MODE_State(True)
			else:
				self._Set_BEAST_MODE_State(False)
			
			if not self._Is_Mob_Alive() and not forceStay and self._Lick_Wounds():
				self.adventure(zone=zone, highest=highest)

			if self._Is_Mob_Alive():
				boss_Is_Alive = self._Is_Boss()
				if (mobs == 0) or \
				(mobs == 1 and boss_Is_Alive) or \
				(mobs == 2 and not boss_Is_Alive):
					if attackType == 2:
						self._Manual_Basic_Attack()
					else:
						attackBool = True if attackType == 1 else False
						self._Manual_Kill(onlyAttack = attackBool)
					if once:
						break
				elif not forceStay:
					# Send left arrow and right arrow to refresh monster.
					win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, wcon.VK_LEFT, 0)
					time.sleep(0.04)
					win32gui.PostMessage(Window.id, wcon.WM_KEYUP, wcon.VK_LEFT, 0)
					time.sleep(0.04)
					win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, wcon.VK_RIGHT, 0)
					time.sleep(0.04)
					win32gui.PostMessage(Window.id, wcon.WM_KEYUP, wcon.VK_RIGHT, 0)
					time.sleep(0.5)
			else:
				time.sleep(0.01)
		self._Set_IdleAttack_State(True)

	def kill_titan(self, target):
		"""Attempt to kill the target titan.

		Keyword arguments:
		target -- The name of the titan you wish to kill. ["GRB", "GCT",
				  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
				  "BEAST4"]
		"""
		self.menu("adventure")
		self._Lick_Wounds()

		self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
		for i in range(ncon.TITAN_ZONE[target]):
			self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, fast=True)

		time.sleep(userset.LONG_SLEEP)

		available = self.ocr(ncon.OCR_ADV_TITANX1, ncon.OCR_ADV_TITANY1,
							 ncon.OCR_ADV_TITANX2, ncon.OCR_ADV_TITANY2)

		if "titan" in available.lower():
			self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
			self._Set_IdleAttack_State(False)
			self._Set_BEAST_MODE_State(False, True)
			for i in range(ncon.TITAN_ZONE[target]):
				self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, fast=True)

			time.sleep(2.6)  # Make sure titans spawn, otherwise loop breaks
			while self._Is_Mob_Alive():
				self._Manual_Kill()
			self._Set_IdleAttack_State(True)
		else:
			return str(available)

	def titan_pt_check(self, target):
		print("not Implemented")
		return
		
		"""Check if we have the recommended p/t to defeat the target Titan.

		Keyword arguments:
		target -- The name of the titan you wish to kill. ["GRB", "GCT",
				  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
				  "BEAST4"]
		"""
		self.menu("adventure")
		bmp = self.get_bitmap()
		power = self.ocr(ncon.OCR_ADV_POWX1, ncon.OCR_ADV_POWY1,
						 ncon.OCR_ADV_POWX2, ncon.OCR_ADV_POWY2, bmp=bmp)
		tough = self.ocr(ncon.OCR_ADV_TOUGHX1, ncon.OCR_ADV_TOUGHY1,
						 ncon.OCR_ADV_TOUGHX2, ncon.OCR_ADV_TOUGHY2, bmp=bmp)

		if (float(power) > ncon.TITAN_PT[target]["p"] and
		   float(tough) > ncon.TITAN_PT[target]["t"]):
			return True

		else:
			print(f"Lacking: {Decimal(ncon.TITAN_PT[target]['p'] - float(power)):.2E}"
				  f"/{Decimal(ncon.TITAN_PT[target]['t'] - float(tough)):.2E} P/T"
				  f" to kill {target}")
			return False

	def adventure(self, zone=0, highest=False, itopod=None, itopodauto=False):
		"""Go to adventure zone to idle.

		Keyword arguments
		zone -- Zone to idle in, 0 is safe zone, 1 is tutorial and so on.
		highest -- If true, will go to your highest available non-titan zone.
		itopod -- If set to true, it will override other settings and will
				  instead enter the specified ITOPOD floor.
		itopodauto -- If set to true it will click the "optimal" floor button.
		"""
		self.menu("adventure")
		if itopod:
			self.click(ncon.ITOPOD_MENU_X, ncon.ITOPOD_MENU_Y)
			if itopodauto:
				self.click(ncon.ITOPOD_AUTO_FLOOR_X, ncon.ITOPOD_AUTO_FLOOR_Y)
				self.click(ncon.ITOPOD_ENTER_X, ncon.ITOPOD_ENTER_Y)
				return
			self.click(ncon.ITOPODSTARTX, ncon.ITOPODSTARTY)
			self.NOV_send_text(itopod)
			self.click(ncon.ITOPODENDX, ncon.ITOPODENDY)
			self.NOV_send_text(itopod)
			self.click(ncon.ITOPOD_ENTER_X, ncon.ITOPOD_ENTER_Y)
			return
		if highest:
			self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, button="right")
			return
		else:
			self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
			for i in range(zone):
				self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, fast=True)
			return


#------------ Inventory ----------------
	def merge_equipment(self):
		"""Navigate to inventory and merge equipment."""
		self.menu("inventory")
		for slot in ncon.EQUIPMENTSLOTS:
			if (slot != "cube"):
				self.click(ncon.EQUIPMENTSLOTS[slot]["x"], ncon.EQUIPMENTSLOTS[slot]["y"])
				self.send_string("d")

	def boost_equipment(self, cube=True):
		"""Boost all equipment."""
		self.menu("inventory")
		for slot in ncon.EQUIPMENTSLOTS:
			if (slot == "cube" and cube):
				self.click(ncon.EQUIPMENTSLOTS[slot]["x"],
						   ncon.EQUIPMENTSLOTS[slot]["y"], "right")
			elif slot != "cube":
				self.click(ncon.EQUIPMENTSLOTS[slot]["x"], ncon.EQUIPMENTSLOTS[slot]["y"])
				self.send_string("a")

	def NOV_boost_equipment(self, whatEquipment):
		self.menu("inventory")
		if whatEquipment == "cube":
			self.click(ncon.EQUIPMENTSLOTS[whatEquipment]["x"], ncon.EQUIPMENTSLOTS[whatEquipment]["y"], "right")
		else:
			self.click(ncon.EQUIPMENTSLOTS[whatEquipment]["x"], ncon.EQUIPMENTSLOTS[whatEquipment]["y"])
			self.send_string("a")

	def get_Inventory_Slot_Pos(self, x, y=1):
		"""Gives the X,Y Pos for inventory slots.
		   x=1 --> first slot in the entire inventory
		   x=1,y=2 --> first slot in the second row
		   x=23 --> last slot in the second row
		   """

		y -= 1
		x -= 1
		if y == 0:
			y = int(x / 12)
			x = x - 12 * y
		return (ncon.NOV_INVENTORY_START_X + ncon.NOV_INVENTORY_OFFSET * x, 
				ncon.NOV_INVENTORY_START_Y + ncon.NOV_INVENTORY_OFFSET * y)

	def loadout(self, target):
		"""Equip targeted loadout."""
		self.menu("inventory")
		self.click(ncon.INVENTORY_LOADOUT_START_X + ncon.INVENTORY_LOADOUT_OFFSET * (target - 1), 
					ncon.INVENTORY_LOADOUT_START_Y)

#------------ Blood Magic --------------
	def blood_magic(self, target):
		"""Assign magic to BM."""
		self.menu("bloodmagic")
		for i in range(target):
			self.click(ncon.BMX, ncon.BMY[i])

	def speedrun_bloodpill(self):
		"""Check if bloodpill is ready to cast."""
		bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
		Autos_Enabled = []
		
		if bm_color == ncon.BM_PILL_READY:
			all_Autos_Off = {}
			for auto in ncon.BM_AUTOS:
				all_Autos_Off[auto] = False		
		
			self.reclaim_all_magic()
			self.reclaim_all_energy()
			self.deactivate_all_diggers()
			
			self.blood_magic(8)
			
			currently_Active_Autos = self.get_Blood_Autos_States()
			self.set_Auto_Blood_Spell(all_Autos_Off)
			start = time.time()
			
			self.time_machine(1e12, magic=True)
			
			if userset.PILL == 0:
				duration = 300
			else:
				duration = userset.PILL
			
			while time.time() < start + duration:
				self.gold_diggers([11])
				time.sleep(5)
				
			self.spells()
			self.click(ncon.BMPILLX, ncon.BMPILLY)
			time.sleep(userset.LONG_SLEEP)
			
			self.set_Auto_Blood_Spell(currently_Active_Autos)
			return True
		else:
			return False
			
	def _Is_Blood_Auto_Active(self, auto):
		self.spells()
		result = self.image_search(ncon.BM_AUTOS[auto]["x"] - 7,
									   ncon.BM_AUTOS[auto]["y"] - 7,
									   ncon.BM_AUTOS[auto]["x"] + 7,
									   ncon.BM_AUTOS[auto]["y"] + 7,
									   self.get_file_path("images", "BMSpellEnabled.png"),
									   0.8)
		return True if result is not None else False

	def get_Blood_Autos_States(self):
		Autos_States = {}
		self.spells()
		for auto in ncon.BM_AUTOS:
			Autos_States[auto] = self._Is_Blood_Auto_Active(auto)
		return Autos_States
		
	def set_Auto_Blood_Spell(self, states):
		for auto in states:
			is_Active = self._Is_Blood_Auto_Active(auto)
			if (is_Active and not states[auto]) or \
				(not is_Active and states[auto]):
				self.click(ncon.BM_AUTOS[auto]["x"], ncon.BM_AUTOS[auto]["y"])
				self.click(10, 10)


#------------ Diggers ------------------
	def NOV_gold_diggers(self, targets, targetValues, activate=False):
		"""Activate diggers.

		Keyword arguments:
		targets -- Array of diggers to use from 1-12. Example: [1, 2, 3, 4, 9].
		targetValues -- Array of digger-Levels to enter, 1-999. Example: [1, 2, 3, 4, 9].
						corresponding with the digger target from targets.
						enter -1 if it should let it stay on the preexisting level
		activate -- Set to True if you wish to activate/deactivate these
					diggers otherwise it will just try to up the cap.
		"""
		self.menu("digger")
		
		for i in range(len(targets)):
			diggerTarget = targets[i]
			diggerValue = targetValues[i]
			page = ((diggerTarget-1)//4)
			item = diggerTarget - (page * 4)
			
			self.click(ncon.DIG_PAGEX[page], ncon.DIG_PAGEY)
			if diggerValue != -1:
				self.click(ncon.DIG_CAP[item]["x"] - 110, ncon.DIG_CAP[item]["y"])
				self.NOV_send_text(diggerValue)
			if activate:
				self.click(ncon.DIG_ACTIVE[item]["x"], ncon.DIG_ACTIVE[item]["y"])

	def gold_diggers(self, targets, deactivate=False):
		"""Activate diggers.

		Keyword arguments:
		targets -- Array of diggers to use from 1-12. Example: [1, 2, 3, 4, 9].
		deactivate -- Set to True if you wish to deactivate these
					diggers otherwise it will just try to up the cap.
		"""
		self.menu("digger")
		for i in targets:
			page = ((i-1)//4)
			item = i - (page * 4)
			self.click(ncon.DIG_PAGEX[page], ncon.DIG_PAGEY)
			if deactivate:
				self.click(ncon.DIG_ACTIVE[item]["x"], ncon.DIG_ACTIVE[item]["y"])
			else:
				self.click(ncon.DIG_CAP[item]["x"], ncon.DIG_CAP[item]["y"])

	def deactivate_all_diggers(self):
		self.menu("digger")
		self.click(ncon.DIG_DEACTIVATE_ALL_X, ncon.DIG_DEACTIVATE_ALL_Y)


#---------------------------------------

	def ygg(self, rebirth=False):
		"""Navigate to inventory and handle fruits."""
		self.menu("yggdrasil")
		if rebirth:
			for i in ncon.FRUITSX:
				self.click(ncon.FRUITSX[i], ncon.FRUITSY[i])
		else:
			self.click(ncon.HARVESTX, ncon.HARVESTY)

	def do_rebirth(self):
		"""Start a rebirth or challenge."""
		self.stop_fight()
		self.rebirth()
		self.click(ncon.REBIRTHBUTTONX, ncon.REBIRTHBUTTONY)
		time.sleep(0.1)
		self.confirm()

	def augments(self, augments, energy):
		"""Dump energy into augmentations.

		Keyword arguments
		augments -- Dictionary that contains which augments you wish to use and
					a ratio that tells how much of the total energy you
					allocated you wish to send. Example:
					{"SS": 0, "DS": 0, "MI": 0, "DTMT": 0, "CI": 0, "M": 0,
					 "SM": 0, "AA": 0, "EB": 0, "CS": 0, "AE": 0, "ES": 0,
					 "LS": 0.9, "QSL": 0.1}
		Energy -- The total amount of energy you want to use for all augments.
		"""
		self.menu("augmentations")
		for k in augments:
			val = math.floor(augments[k] * energy)
			self.input_box()
			self.NOV_send_text(val)
			# Scroll down if we have to.
			bottom_augments = ["AE", "ES", "LS", "QSL"]
			i = 0
			if (k in bottom_augments):
				color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
											 ncon.SANITY_AUG_SCROLLY_BOT)
				while color not in ncon.SANITY_AUG_SCROLL_COLORS:
					self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLBOTY)
					time.sleep(userset.MEDIUM_SLEEP)
					color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
												 ncon.SANITY_AUG_SCROLLY_BOT)
					i += 1
					if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
						Navigation.current_menu = ""
						self.menu("augmentations")
					elif i > 10:
						print("Couldn't assign augments")
						break

			else:
				color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
											 ncon.SANITY_AUG_SCROLLY_TOP)
				while color not in ncon.SANITY_AUG_SCROLL_COLORS:
					self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLTOPY)
					time.sleep(userset.MEDIUM_SLEEP)
					color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
												 ncon.SANITY_AUG_SCROLLY_TOP)
					i += 1
					if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
						Navigation.current_menu = ""
						self.menu("augmentations")
					elif i > 10:
						print("Couldn't assign augments")
						break
			self.click(ncon.AUGMENTX, ncon.AUGMENTY[k])

	def time_machine(self, e, m=0, magic=False):
		"""Add energy and/or magic to TM.
		Example: self.time_machine(1000, 2000)
				 self.time_machine(1000, magic=True)
				 self.time_machine(1000)

		First example will add 1000 energy and 2000 magic to TM.
		Second example will add 1000 energy and 1000 magic to TM.
		Third example will add 1000 energy to TM.

		Keyword arguments:
		e -- The amount of energy to put into TM.
		m -- The amount of magic to put into TM, if this is 0, it will use the
			 energy value to save unnecessary clicks to the input box.
		magic -- Set to true if you wish to add magic as well"""
		self.menu("timemachine")
		self.input_box()
		self.NOV_send_text(e)
		self.click(ncon.TMSPEEDX, ncon.TMSPEEDY)
		if magic or m:
			if m != 0:
				self.input_box()
				self.NOV_send_text(m)
			self.click(ncon.TMMULTX, ncon.TMMULTY)

	def wandoos(self, magic=False):
		"""Assign energy and/or magic to wandoos."""
		self.menu("wandoos")
		self.click(ncon.WANDOOS_CAP_X, ncon.WANDOOS_ENERGY_BUTTONS_Y)
		if magic:
			self.click(ncon.WANDOOS_CAP_X, ncon.WANDOOS_MAGIC_BUTTONS_Y)

	def wandoos_amount(self, e, m):
		self.menu("wandoos")
		if e != 0:
			self.input_box()
			self.NOV_send_text(abs(e))
			if e > 0: #Add to Energy
				self.click(ncon.WANDOOS_ADD_X, ncon.WANDOOS_ENERGY_BUTTONS_Y)
			elif e < 0: #Reduce from Energy
				self.click(ncon.WANDOOS_MINUS_X, ncon.WANDOOS_ENERGY_BUTTONS_Y)
		
		if m == 0:
			return
		
		if abs(e) != abs(m): #if the value is the same for magic as energy, no need to insert the value again
			self.input_box()
			self.NOV_send_text(abs(m))
			
		if m > 0: #Add to Magic
			self.click(ncon.WANDOOS_ADD_X, ncon.WANDOOS_MAGIC_BUTTONS_Y)
		else: #Reduce from Magic
			self.click(ncon.WANDOOS_MINUS_X, ncon.WANDOOS_MAGIC_BUTTONS_Y)

	def assign_ngu(self, value, targets, magic=False):
		"""Assign energy/magic to NGU's.

		Keyword arguments:
		value -- the amount of energy/magic that will get split over all NGUs.
		targets -- Array of NGU's to use (1-9).
		magic -- Set to true if these are magic NGUs
		"""
		if len(targets) > 9:
			raise RuntimeError("Passing too many NGU's to assign_ngu," +
							   " allowed: 9, sent: " + str(len(targets)))
		if magic:
			self.ngu_magic()
		else:
			self.menu("ngu")

		self.input_box()
		self.NOV_send_text(str(int(value // len(targets))))
		for i in targets:
			self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + i * 35)

	def bb_ngu(self, value, targets, overcap=1, magic=False):
		"""Estimates the BB value of each supplied NGU.

		Keyword arguments:
		targets -- Array of NGU's to BB. Example: [1, 3, 4, 5, 6]
		magic -- Set to true if these are magic NGUs
		"""
		if magic:
			self.ngu_magic()
		else:
			self.menu("ngu")

		self.input_box()
		self.NOV_send_text(value)

		for target in targets:
			self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + target * 35)

		for target in targets:
			energy = 0
			for x in range(198):
				color = self.get_pixel_color(ncon.NGU_BAR_MINX + x,
											 ncon.NGU_BAR_Y +
											 ncon.NGU_BAR_OFFSETY * target,
											 )
				if color == ncon.NGU_BAR_WHITE:
					pixel_coefficient = x / 198
					value_coefficient = overcap / pixel_coefficient
					energy = (value_coefficient * value) - value
					
					#total_Needed = (value_coefficient * value)
					#print(f"estimated energy to BB this NGU is {Decimal(total_Needed):.2E}")
					break
			if energy > 0:
				self.input_box()
				self.NOV_send_text(energy)
				self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + target * 35)

	def advanced_training(self, value, wandoos=0):
		self.menu("advtraining")
		self.input_box()
		self.NOV_send_text(value)
		self.click(ncon.ADV_TRAINING_ADD_X, ncon.ADV_TRAINING_ADD_Y)
		self.click(ncon.ADV_TRAINING_ADD_X, ncon.ADV_TRAINING_ADD_Y + ncon.ADV_TRAINING_ADD_Y_OFFSET)
		
		if wandoos > 0:
			if wandoos > 1 and wandoos != value:
				self.input_box()
				self.NOV_send_text(wandoos)
			self.click(ncon.ADV_TRAINING_ADD_X, ncon.ADV_TRAINING_ADD_Y + 3 * ncon.ADV_TRAINING_ADD_Y_OFFSET)
			self.click(ncon.ADV_TRAINING_ADD_X, ncon.ADV_TRAINING_ADD_Y + 4 * ncon.ADV_TRAINING_ADD_Y_OFFSET)
			
	def save_check(self):
		"""Check if we can do the daily save for AP.

		Make sure no window in your browser pops up when you click the "Save"
		button, otherwise sit will mess with the rest of the script.
		"""
		color = self.get_pixel_color(ncon.SAVEX, ncon.SAVEY)
		if color == ncon.SAVE_READY_COLOR:
			self.click(ncon.SAVEX, ncon.SAVEY)
		return

	def get_inventory_slots(self, slots):
		"""Get coords for inventory slots from 1 to slots."""
		point = namedtuple("p", ("x", "y"))
		i = 1
		row = 1
		x_pos = ncon.INVENTORY_SLOTS_X
		y_pos = ncon.INVENTORY_SLOTS_Y
		coords = []

		while i <= slots:
			x = x_pos + (i - (12 * (row - 1))) * 50
			y = y_pos + ((row - 1) * 50)
			coords.append(point(x, y))
			if i % 12 == 0:
				row += 1
			i += 1
		return coords

	def merge_inventory(self, slots):
		"""Merge all inventory slots starting from 1 to slots.

		Keyword arguments:
		slots -- The amount of slots you wish to merge
		"""
		self.menu("inventory")
		coords = self.get_inventory_slots(slots)
		for slot in coords:
			self.click(slot.x, slot.y)
			self.send_string("d")

	def boost_inventory(self, slots):
		"""Merge all inventory slots starting from 1 to slots.
		
		start on slot 1(not zero based) and iterates up towards *slots*

		Keyword arguments:
		slots -- The amount of slots you wish to merge
		"""
		self.menu("inventory")
		coords = self.get_inventory_slots(slots)
		for slot in coords:
			self.click(slot.x, slot.y)
			self.send_string("a")

	def transform_slot(self, slot, threshold=0.8, consume=False):
		"""Check if slot is transformable and transform if it is.

		Be careful using this, make sure the item you want to transform is
		not protected, and that all other items are protected, this might
		delete items otherwise. Another note, consuming items will show
		a special tooltip that will block you from doing another check
		for a few seconds, keep this in mind if you're checking multiple
		slots in succession.

		Keyword arguments:
		slot -- The slot you wish to transform, if possible
		threshold -- The fuzziness in the image search, I recommend a value
					 between 0.7 - 0.95.
		consume -- Set to true if item is consumable instead.
		"""
		raise RuntimeError("Not implemented")
		
		self.menu("inventory")
		slot = self.get_inventory_slots(slot)[-1]
		self.click(*slot)
		time.sleep(userset.SHORT_SLEEP)

		if consume:
			coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, self.get_file_path("images", "consumable.png"), threshold)
		else:
			coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, self.get_file_path("images", "transformable.png"), threshold)

		if coords:
			self.ctrl_click(*slot)

			
#-------------- Questing ---------------

	def get_Quest_Text(self):
		self.menu("questing")
		self.click(10, 10)
		text = self.ocr(ncon.QUESTING_DESCRIPTION_X1, ncon.QUESTING_DESCRIPTION_Y1, 
						ncon.QUESTING_DESCRIPTION_X2, ncon.QUESTING_DESCRIPTION_Y2, debug=False)
		text = text.lower()
		text = text.replace("\n", " ")
		return text
		
	def collect_Quest_Items(self, questZone, clean_up=False):
		self.menu("inventory")
		result = self.image_search(ncon.INVENTORY_GRID_REGION_X1,
								   ncon.INVENTORY_GRID_REGION_Y1,
								   ncon.INVENTORY_GRID_REGION_X2,
								   ncon.INVENTORY_GRID_REGION_Y2,
								   self.get_file_path("images", ncon.QUESTING_ZONES[questZone]["filename"]),
								   0.9, debug=False)

		if result != None:
			item_X = ncon.INVENTORY_GRID_REGION_X1 + result[0] + 20
			item_Y = ncon.INVENTORY_GRID_REGION_Y1 + result[1] + 20
		
			if clean_up:
				self.click(item_X, item_Y)
				self.send_string("d")
				self.click(item_X, item_Y, button="right", ctrl=True)
			else: #Normal
				self.click(item_X, item_Y, button="right")

	def questing(self, duration=60):
		quest_Text = self.get_Quest_Text()

		if "handed in" in quest_Text: #Quest is completed
			self.click(ncon.QUESTING_COMPLETE_BUTTON_X, ncon.QUESTING_COMPLETE_BUTTON_Y) #Hands in the Quest
			time.sleep(userset.LONG_SLEEP)
			self.click(ncon.QUESTING_COMPLETE_BUTTON_X, ncon.QUESTING_COMPLETE_BUTTON_Y) #Starts a new Quest
			quest_Text = self.get_Quest_Text()

		if "start quest" in quest_Text: #No Quest is active
			self.click(ncon.QUESTING_COMPLETE_BUTTON_X, ncon.QUESTING_COMPLETE_BUTTON_Y) #Starts a new Quest
			quest_Text = self.get_Quest_Text()

		if not "major quest" in quest_Text:
			print("Completed all Major Quests")
			return False

		questZone = "?"
		for name in ncon.QUESTING_ZONES:
			if name in quest_Text:
				questZone = name
		if questZone == "?":
			raise RuntimeError(f"Find no quest zone in \"{quest_Text}\"")



		farm_start = time.time()
		self.adventure(zone=ncon.QUESTING_ZONES[questZone]["floor"])

		while not "handed in" in quest_Text: #while quest not done
			self.snipe_hard(0, duration, mobs=0, attackType=2, forceStay=True)

			'''
			self.menu("inventory")
			i.click(10, 10)
			aaa = self.get_bitmap()
			aaa.save("Pic\\questing_" + str(int(time.time())) + ".png")
			'''

			self.collect_Quest_Items(questZone)
			self.NOV_boost_equipment("cube")
			quest_Text = self.get_Quest_Text()


		#duration_sec = round(time.time() - farm_start)	
		#duration_converted = str(datetime.timedelta(seconds=duration_sec))
		duration_converted = str(datetime.timedelta(seconds=round(time.time() - farm_start)))
		print(f"It took {duration_converted} to complete the Quest")
		self.menu("questing")
		self.click(ncon.QUESTING_COMPLETE_BUTTON_X, ncon.QUESTING_COMPLETE_BUTTON_Y)
		self.collect_Quest_Items(questZone, True)
		return True

#-------------- Misc -------------------

	def get_rebirth_time(self, bmp=None):
		#Stolen from @migetno1#4481 in discord. Credit to him/her

		the_time = self.ocr(37, 387, 146, 408, False, bmp)
		#x = re.search("((?P<days>[0-9]) day )?((?P<hours>[0-9]+):)?(?P<minutes>[0-9]+):(?P<seconds>[0-9]+)", the_time)
		x = re.search("((?P<days>[0-9]+) days? )?((?P<hours>[0-9]+):)?(?P<minutes>[0-9]+):(?P<seconds>[0-9]+)", the_time)
		seconds = 0
		
		if x is not None:
			if x.group('days') is not None:
				seconds += 24 * 60 * int(x.group('days')) * 60

			if x.group('hours') is not None:
				seconds += 60 * 60 * int(x.group('hours'))

			if x.group('minutes') is not None:
				seconds += int(x.group('minutes')) * 60

			if x.group('seconds') is not None:
				seconds += int(x.group('seconds'))

		return seconds