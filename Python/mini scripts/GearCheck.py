


def addItem(name, slot, stats):
	id = len(items)
	items[id] = {}
	items[id]["name"] = name
	items[id]["slot"] = slot
	items[id]["E-Pow"] = 0
	items[id]["M-Pow"] = 0
	items[id]["E-Cap"] = 0
	items[id]["M-Cap"] = 0
	
	for var in stats:
		split = var.split("-")
		energy = "E" in split[0]
		magic = "M" in split[0]
		
		if split[1] == "Pow":
			if energy:
				items[id]["E-Pow"] += stats[var]
			if magic:
				items[id]["M-Pow"] += stats[var]
		elif split[1] == "Cap":
			if energy:
				items[id]["E-Cap"] += stats[var]
			if magic:
				items[id]["M-Cap"] += stats[var]


items = {}
addItem("Clown Hat", "head", {"M-Pow":11000, "EM-Cap":1100, "EM-Bar":7000})
addItem("Fabulous Super Chest", "chest", {"EM-Cap":1100, "EM-Pow":10800, "M-Bar":10600})
addItem("A Crappy Tutu", "legs", {"E-Bar":10000, "E-Pow":14000, "EM-Cap":1200})
addItem("Pretty Pink Slippers", "boots", {"M-Cap":1260, "M-Bar":10000, "EM-Pow":13000})
addItem("Giant Sticky Foot", "weapon", {"E-Cap":1140, "EM-Pow":12000, "M-Bar":6600})



total = 0
for i in items:
	val = items[i]["E-Pow"]
	total += items[i]["E-Pow"]
	
	print(f"{i} - {val}")
print(str(total))




"""
QUESTING_ZONES = {"sewers": {"filename": "Sewers.png", "floor": 2}, #key is case sensitive
				  "forest": {"filename": "Forest.png", "floor": 3},
				  "security": {"filename": "High Security Base.png", "floor": 6},
				  "universe": {"filename": "The 2D Universe.png", "floor": 10},
				  "strange": {"filename": "A Very Strange Place.png", "floor": 13},
				  "megaland": {"filename": "Mega Lands.png", "floor": 14},
				  "beardverse": {"filename": "The Beardverse.png", "floor": 16},
				  "chocolate": {"filename": "Chocolate World.png", "floor": 21},
				  "evilverse": {"filename": "Evilverse.png", "floor": 22}}
"""