bestMagic = 0
bestEnergy = 0
bestValue = 0

MaxLevels = 30


val = 0

def calc(energy, magic):
	return round((1 + (energy / 5)) * (1 + (magic * 2)),2)

for testMagic in range(MaxLevels):
	for testEnergy in range(MaxLevels):
		if (testMagic + testEnergy) > MaxLevels:
			continue
		val = calc(testEnergy, testMagic)
		print(f"e:{testEnergy} m:{testMagic} val:{val}")
		if val > bestValue:
			bestMagic = testMagic
			bestEnergy = testEnergy
			bestValue = val
			
print("----------------------------------------------")
bestValue *= 100
bestValue = int(bestValue)
print(f"e:{bestEnergy} m:{bestMagic} val:{bestValue}%")