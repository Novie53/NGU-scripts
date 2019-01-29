"""Buys things for exp."""
from classes.stats import NOV_Tracker
import ngucon as ncon
import usersettings as userset
import time


class Upgrade(NOV_Tracker):
	"""Buys things for exp."""

	def __init__(self, ecap, mcap, ebar, mbar, e2m_ratio):
		"""Example: Upgrade(37500, 37500, 2, 1).

		This will result in a 1:37500:2 ratio for energy and 1:37500:1 for
		magic. i.e. 1 power, 37500 ecap and 2 ebars.

		Keyword arguments:

		ecap -- The amount of energy cap in the ratio. Must be over 10000 and
				divisible by 250.
		mcap -- The amount of magic cap in the ratio. Must be over 10000 and
				divisible by 250.
		ebar -- the amount of energy bars to buy in relation to power
		mbar -- the amount of magic bars to buy in relation to power.
		e2m_ratio -- The amount of exp to spend in energy in relation to magic.
					 a value of 5 will buy 5 times more upgrades in energy than
					 in magic, maintaining a 5:1 E:M ratio.
		"""
		self.ecap = ecap
		self.mcap = mcap
		self.ebar = ebar
		self.mbar = mbar
		self.e2m_ratio = e2m_ratio

	def em(self):
		"""Buy upgrades for both energy and magic.

		Requires the confirmation popup button for EXP purchases in settings
		to be turned OFF.

		This uses all available exp, so use with caution.
		"""
		if self.ecap < 10000 or self.ecap % 250 != 0:
			print("Ecap value not divisible by 250 or lower than 10000, not" +
				  " spending exp.")
			return
		if self.mcap < 10000 or self.mcap % 250 != 0:
			print("Mcap value not divisible by 250 or lower than 10000, not" +
				  " spending exp.")
			return

		current_XP = self.__get_stat("XP")

		e_cost = ncon.EPOWER_COST + ncon.ECAP_COST * self.ecap + (
				 ncon.EBAR_COST * self.ebar)

		m_cost = ncon.MPOWER_COST + ncon.MCAP_COST * self.mcap + (
				 ncon.MBAR_COST * self.mbar)

		total_price = m_cost + self.e2m_ratio * e_cost

		"""Skip upgrading if we don't have enough exp to buy at least one
		complete set of upgrades, in order to maintain our perfect ratios :)"""

		if total_price > current_XP:
			return

		amount = int(current_XP // total_price)

		e_power = int(amount * self.e2m_ratio)
		e_cap = int(amount * self.ecap * self.e2m_ratio)
		e_bars = int(amount * self.ebar * self.e2m_ratio)
		m_power = int(amount)
		m_cap = int(amount * self.mcap)
		m_bars = int(amount * self.mbar)

		self.exp()

		self.click(ncon.EMPOWBOXX, ncon.EMBOXY)
		self.NOV_send_text(e_power)
		time.sleep(userset.MEDIUM_SLEEP)

		self.click(ncon.EMCAPBOXX, ncon.EMBOXY)
		self.NOV_send_text(e_cap)
		time.sleep(userset.MEDIUM_SLEEP)

		self.click(ncon.EMBARBOXX, ncon.EMBOXY)
		self.NOV_send_text(e_bars)
		time.sleep(userset.MEDIUM_SLEEP)

		self.click(ncon.EMPOWBUYX, ncon.EMBUYY)
		self.click(ncon.EMCAPBUYX, ncon.EMBUYY)
		self.click(ncon.EMBARBUYX, ncon.EMBUYY)

		self.exp_magic()

		self.click(ncon.EMPOWBOXX, ncon.EMBOXY)
		self.NOV_send_text(m_power)
		time.sleep(userset.MEDIUM_SLEEP)

		self.click(ncon.EMCAPBOXX, ncon.EMBOXY)
		self.NOV_send_text(m_cap)
		time.sleep(userset.MEDIUM_SLEEP)

		self.click(ncon.EMBARBOXX, ncon.EMBOXY)
		self.NOV_send_text(m_bars)
		time.sleep(userset.MEDIUM_SLEEP)

		self.click(ncon.EMPOWBUYX, ncon.EMBUYY)
		self.click(ncon.EMCAPBUYX, ncon.EMBUYY)
		self.click(ncon.EMBARBUYX, ncon.EMBUYY)

		self.set_value_with_ocr("XP")

