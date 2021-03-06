"""Handles various statistics."""
from classes.navigation import Navigation

import ngucon as ncon
import time
import datetime


#https://pyformat.info/
#https://scientificallysound.org/2016/10/17/python-print3/


class NOV_Tracker(Navigation):

	def __init__(self):
		self.__start_time = time.time()
		self.__iteration = 1
		self.total_XP_gained = 0
		self.total_PP_gained = 0
		
		self.currXP = self.get_stat("XP")
		self.currPP = self.get_stat("PP")
		
		self.__printTopRow()
		print('Starting: {:^8}{:^3}Starting: {:^8}'.format(self.__human_format(self.currXP), "|", 
															self.__human_format(self.currPP)))

	def update_progress(self, display=True):
		self.__iteration += 1
		
		newXP = self.get_stat("XP")
		newPP = self.get_stat("PP")
		XP_this_run = 0
		PP_this_run = 0
		
		if newXP != -1:#XP OCR success
			XP_this_run = newXP - self.currXP
			self.currXP = newXP
			self.total_XP_gained += XP_this_run
			
		if newPP != -1:#PP OCR success
			PP_this_run = newPP - self.currPP
			self.currPP = newPP
			self.total_PP_gained += PP_this_run
		
		if display:
			self.__display_progress(XP_this_run, PP_this_run)
			
			self.__printTopRow()

	def adjustxp(self):
		self.currXP = self.get_stat("XP")
		self.currPP = self.get_stat("PP")

	def get_stat(self, value):
		try:
			if value == "TOTAL XP":
				self.misc()
				return int(float(self.ocr(ncon.OCR_EXPX1, ncon.OCR_EXPY1, ncon.OCR_EXPX2, ncon.OCR_EXPY2)))
			elif value == "XP":
				self.exp()
				return int(self.remove_letters(self.ocr(ncon.EXPX1, ncon.EXPY1, ncon.EXPX2, ncon.EXPY2)))
			elif value == "PP":
				self.perks()
				return int(self.remove_letters(self.ocr(ncon.PPX1, ncon.PPY1, ncon.PPX2, ncon.PPY2)))
		except ValueError:
			print(f"Failed to get data for {value}")
			return -1




	def __display_progress(self, XP_this_run, PP_this_run):
		duration_sec = round(time.time() - self.__start_time)
		XP_per_Hour = self.total_XP_gained / (duration_sec / 3600)
		PP_per_Hour = self.total_PP_gained / (duration_sec / 3600)		
		duration_converted = str(datetime.timedelta(seconds=duration_sec))
		
		print("This run: {:^8}{:^3}This run: {:^8}".format(self.__human_format(XP_this_run), "|", self.__human_format(PP_this_run)))
		print('Current:  {:^8}{:^3}Current:  {:^8}'.format(self.__human_format(self.currXP), "|", self.__human_format(self.currPP)))
		print('Total:    {:^8}{:^3}Total:    {:^8}'.format(self.__human_format(self.total_XP_gained), "|", self.__human_format(self.total_PP_gained)))
		print('Per hour: {:^8}{:^3}Per hour: {:^8}'.format(self.__human_format(XP_per_Hour), "|", self.__human_format(PP_per_Hour)))
		print("\n{0:^40}\n".format(duration_converted))
	
	def __printTopRow(self):
		print("{0:{fill}{align}40}".format(f" {self.__iteration} ", fill="-", align="^"))
		print("{:^18}{:^3}{:^18}".format("XP", "|", "PP"))
		print("-" * 40)

	def __human_format(self, num):
		if num <= 100 and num > 0:
			return round(num, 2)

		num = float('{:.3g}'.format(num))
		if num > 1e14:
			return
		magnitude = 0
		while abs(num) >= 1000:
			magnitude += 1
			num /= 1000.0
		return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


'''
		
		
		
class Stats(Navigation):
	"""Handles various statistics."""

	total_xp = 0
	xp = 0
	pp = 0
	start_time = time.time()
	OCR_failures = 0
	OCR_failed = False
	track_xp = True
	track_pp = True

	def set_value_with_ocr(self, value):
		"""Store start EXP via OCR."""
		try:
			if value == "TOTAL XP":
				self.misc()
				Stats.total_xp = int(float(self.ocr(ncon.OCR_EXPX1, ncon.OCR_EXPY1, ncon.OCR_EXPX2, ncon.OCR_EXPY2)))
				# print("OCR Captured TOTAL XP: {:,}".format(Stats.total_xp))
			elif value == "XP":
				self.exp()
				Stats.xp = int(self.remove_letters(self.ocr(ncon.EXPX1, ncon.EXPY1, ncon.EXPX2, ncon.EXPY2)))
				# print("OCR Captured Current XP: {:,}".format(Stats.xp))
			elif value == "PP":
				self.perks()
				Stats.pp = int(self.remove_letters(self.ocr(ncon.PPX1, ncon.PPY1, ncon.PPX2, ncon.PPY2)))
				# print("OCR Captured Current PP: {:,}".format(Stats.pp))
			Stats.OCR_failed = False
			Stats.OCR_failures = 0
		except ValueError:
			Stats.OCR_failures += 1
			if Stats.OCR_failures <= 3:
				print("OCR couldn't detect {}, retrying.".format(value))
				if Stats.OCR_failures >= 2:
					print("Clearing Navigation.current_menu")
					Navigation.current_menu = ""
				self.set_value_with_ocr(value)
			else:
				print("Something went wrong with the OCR")
				Stats.OCR_failures = 0
				Stats.OCR_failed = True

class EstimateRate(Stats):

	def __init__(self, duration, mode='moving_average'):
		self.mode = mode
		self.last_timestamp = time.time()
		if Stats.track_xp:
			self.set_value_with_ocr("XP")
		self.last_xp = Stats.xp
		if Stats.track_pp:
			self.set_value_with_ocr("PP")
		self.last_pp = Stats.pp
		# Differential time log and value
		self.dtime_log = []
		self.dxp_log = []
		self.dpp_log = []
		# Num runs to keep for moving average
		self.__keep_runs = 60 // duration
		self.__iteration = 0
		self.__elapsed = 0
		self.__alg = {
			'moving_average': self.__moving_average,
			'average': self.__average
		}

	def __average(self):
		"""Returns the average rates"""
		avg_xp = sum(self.dxp_log) / sum(self.dtime_log)
		avg_pp = sum(self.dpp_log) / sum(self.dtime_log)
		return avg_xp, avg_pp

	def __moving_average(self):
		"""Returns the moving average rates"""
		if len(self.dtime_log) > self.__keep_runs:
			self.dtime_log.pop(0)
			if Stats.track_xp:
				self.dxp_log.pop(0)
			if Stats.track_pp:
				self.dpp_log.pop(0)
		avg_xp = sum(self.dxp_log) / sum(self.dtime_log)
		avg_pp = sum(self.dpp_log) / sum(self.dtime_log)
		return avg_xp, avg_pp

	def rates(self):
		try:
			xpr, ppr = self.__alg[self.mode]()
			return round(3600*xpr), round(3600*ppr)
		except ZeroDivisionError:
			return 0, 0

	def stop_watch(self):
		"""This method needs to be called for rate estimations"""
		self.__iteration += 1
		if Stats.track_xp:
			self.set_value_with_ocr("XP")
			if not Stats.OCR_failed:
				cxp = Stats.xp
				dxp = cxp - self.last_xp
				self.dxp_log.append(dxp)
				self.last_xp = cxp
			else:
				print("Problems with OCR, skipping stats for this run")
				self.last_timestamp = time.time()
				return
		if Stats.track_pp:
			self.set_value_with_ocr("PP")
			if not Stats.OCR_failed:
				cpp = Stats.pp
				dpp = cpp - self.last_pp
				self.dpp_log.append(dpp)
				self.last_pp = cpp
			else:
				print("Problems with OCR, skipping stats for this run")
				self.last_timestamp = time.time()
				return
		dtime = time.time() - self.last_timestamp
		self.dtime_log.append(dtime)
		self.last_timestamp = time.time()
		print("This run: {:^8}{:^3}This run: {:^8}".format(Tracker.human_format(dxp), "|", Tracker.human_format(dpp)))

	def update_xp(self):
		"""This method is used to update last xp after upgrade spends"""
		self.last_xp = Stats.xp


class Tracker():
	"""
	The Tracker object collects time and value measurements for stats

	Usage: Initialize the class by calling tracker = Tracker(duration),
		   then at the end of each run invoke tracker.progress() to update stats.
	"""

	def __init__(self, duration, track_xp=True, track_pp=True, mode='moving_average'):
		self.__start_time = time.time()
		self.__iteration = 1
		Stats.track_xp = track_xp
		Stats.track_pp = track_pp
		self.__estimaterate = EstimateRate(duration, mode)
		#print(f"{'-' * 15} Run # {self.__iteration} {'-' * 15}")
		print("{0:{fill}{align}40}".format(f" {self.__iteration} ", fill="-", align="^"))
		print("{:^18}{:^3}{:^18}".format("XP", "|", "PP"))
		print("-" * 40)
		self.__show_progress()


	def __update_progress(self):
		self.__iteration += 1

	def __show_progress(self):
		if self.__iteration == 1:
			print('Starting: {:^8}{:^3}Starting: {:^8}'.format(self.human_format(Stats.xp), "|", self.human_format(Stats.pp)))
		else:
			elapsed = self.elapsed_time()
			xph, pph = self.__estimaterate.rates()
			report_time = "\n{0:^40}\n".format(elapsed)
			print('Current:  {:^8}{:^3}Current:  {:^8}'.format(self.human_format(Stats.xp), "|", self.human_format(Stats.pp)))
			print('Per hour: {:^8}{:^3}Per hour: {:^8}'.format(self.human_format(xph), "|", self.human_format(pph)))
			print(report_time)

	def elapsed_time(self):
		"""Print the total elapsed time."""
		elapsed = round(time.time() - self.__start_time)
		elapsed_time = str(datetime.timedelta(seconds=elapsed))
		return elapsed_time

	def progress(self):
			self.__estimaterate.stop_watch()
			self.__update_progress()
			if not Stats.OCR_failed:
				self.__show_progress()
			print("{0:{fill}{align}40}".format(f" {self.__iteration} ", fill="-", align="^"))
			print("{:^18}{:^3}{:^18}".format("XP", "|", "PP"))
			print("-" * 40)

	def adjustxp(self):
			self.__estimaterate.update_xp()

	@classmethod
	def human_format(self, num):
		num = float('{:.3g}'.format(num))
		if num > 1e14:
			return
		magnitude = 0
		while abs(num) >= 1000:
			magnitude += 1
			num /= 1000.0
		return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
		
		
		
'''