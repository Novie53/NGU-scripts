import time
import datetime

Max = 10
Current = 6
TimeLeft = "0:3" #"Hours:Minutes" for example "1:24"
Reduced_Time_Buff = False



split = TimeLeft.split(":")
TimeLeft_Sec = (int(split[0]) * 60 + int(split[1])) * 60
multiplier = 0.8 if Reduced_Time_Buff else 1
total_TimeLeft_sec = TimeLeft_Sec + (Max - (Current + 1)) * (8 * 60 * 60) * multiplier


def convertTime(Sectime):
	hours = int(Sectime / 3600)
	min = int((Sectime - hours * 3600) / 60)
	if hours < 10:
		hours = f"0{hours}"
	if min < 10:
		min = f"0{min}"
	return f"{hours}:{min}"
		


delta = datetime.timedelta(seconds=total_TimeLeft_sec)
then = datetime.datetime.now() + delta

print("hours left until all major quest are ready:", convertTime(delta.total_seconds()))
print("All major quest will be ready at:", then.strftime("%Y-%m-%d %H:%M"))