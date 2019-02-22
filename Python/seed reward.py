import math



Fruit_Base_Seed_Reward = {1:1,
						  2:1,
						  3:1,
						  4:1,
						  5:10,
						  6:1,
						  7:1,
						  8:3,
						  9:3,
						  10:5,
						  11:6,
						  12:7}
						  #13:1}#Not verified
Fruit_Base_Cost = {1:1,
				   2:10,
				   3:25,
				   4:40,
				   5:60,
				   6:100,
				   7:150,
				   8:170,
				   9:200,
				   10:2000,
				   11:20000,
				   12:30000,
				   13:50000,
				   14:100000}
First_Harvest_Perk_Levels = 5
Seed_Reward_Perk_Levels = 20 #20 = Max
Seed_Reward_Quirks_Levels = 25# 25 = Max
Equipment_Seed_Reward = 143 #%
Equipment_Yeild_Reward = 10.6 #%
NGU_Seed_Reward = 1123.4 #%
current_fruits = {1: {"t":24, "h":True, "p":False}, #Gold
				  2: {"t":24, "h":True, "p":False}, #Power Alpha
				  3: {"t":24, "h":False, "p":False}, #Adven
				  4: {"t":24, "h":True, "p":False}, #Know
				  5: {"t":24, "h":True, "p":True}, #Pom
				  6: {"t":23, "h":False, "p":False}, #Luck
				  7: {"t":7, "h":True, "p":False}, #Power Beta
				  8: {"t":10, "h":False, "p":False}, #Arb
				  9: {"t":8, "h":True, "p":False}, #Numbers
				  10: {"t":3, "h":False, "p":False}, #Rage
				  11: {"t":1, "h":False, "p":False}, #Macguffin
				  12: {"t":1, "h":False, "p":False}} #Power Omega
current_seed_count = 6951


#TODO påverkar Equipment_Yeild_Reward någon av seed rewardsen?
def get_seed_reward(fruit, tier, harvest = False, first_Harvest = False, poop = False):
	if tier > 24 or tier < 1:
		print("out of bounds")
		return 0

	a = math.ceil(pow(tier, 1.5))
	a *= Fruit_Base_Seed_Reward[fruit]
	a *= (1 + First_Harvest_Perk_Levels / 10) if first_Harvest else 1
	a *= 1 + Seed_Reward_Perk_Levels * 0.05
	a *= 1 + Seed_Reward_Quirks_Levels * 0.01
	a *= 1 + (Equipment_Seed_Reward / 100)
	a *= (NGU_Seed_Reward / 100)
	#a *= 1 + (Equipment_Yeild_Reward / 100)
	a *= 2 if (harvest and fruit != 5) else 1#Pomegranate is not effect by harvest/eat
	a *= 1.5 if poop else 1
	a = math.ceil(a)
	
	return a

def get_eat_reward(fruit, tier, first_Harvest = False, poop = False):
	a = math.ceil(pow(tier, 1.5))
	a *= (1 + First_Harvest_Perk_Levels / 10) if first_Harvest else 1
	if fruit == 1:
		a *= 30
	return a

def get_upgrade_cost(fruit, currentTier):
	if currentTier >= 24:
		return 0
	return pow(currentTier + 1, 2) * Fruit_Base_Cost[fruit]

def get_daily_seeds(fruit, tier):
	if tier == 24:
		return get_seed_reward(fruit, tier, current_fruits[fruit]["h"], True, current_fruits[fruit]["p"])
	else:
		hours_left = 24
		seed_count = 0
		seed_count += get_seed_reward(fruit, tier, current_fruits[fruit]["h"], True, False)
		hours_left -= tier
		
		while True:
			if hours_left > tier:
				seed_count += get_seed_reward(fruit, tier, current_fruits[fruit]["h"], False, False)
				hours_left -= tier
			else:
				seed_count += get_seed_reward(fruit, hours_left, current_fruits[fruit]["h"], False, False)
				break
		return seed_count
		
def get_max_efford_upgrades(fruit, currentTier, seed_count):
	upgrades = 0
	total_cost = 0
	while True:
		next_upgrade_cost = get_upgrade_cost(fruit, currentTier + upgrades)
		if (currentTier + upgrades) == 24:
			return upgrades, total_cost
		if next_upgrade_cost > seed_count:
			return upgrades, total_cost
		else:
			upgrades += 1
			total_cost += next_upgrade_cost
			seed_count -= next_upgrade_cost



#abctier = 5
#print(str(get_seed_reward(abctier, current_fruits[abctier]["t"], current_fruits[abctier]["h"], True, current_fruits[fruit]["p"])))
#exit()

dailySeed = 0
seedRewards = []
for fruit in current_fruits:
	current_seed = get_daily_seeds(fruit, current_fruits[fruit]["t"])
	dailySeed += current_seed
	seedRewards.append(current_seed)
print(str(dailySeed))
for i in range(len(seedRewards)):
	procent = round(seedRewards[i] / dailySeed, 2)
	print(f"{i+1}\t{procent}%\t{seedRewards[i]}")
	#print(str(i + 1))
exit()



best_fruit = 0
best_ROI = 0

#for fruit in range(1, 12):
for fruit in current_fruits:
	if current_fruits[fruit]["t"] == 24:
		continue
	upgrades, totalCost = get_max_efford_upgrades(fruit, current_fruits[fruit]["t"], current_seed_count)
	current_seed_reward = get_daily_seeds(fruit, current_fruits[fruit]["t"])
	next_seed_reward = get_daily_seeds(fruit, current_fruits[fruit]["t"] + upgrades)
	diff = next_seed_reward - current_seed_reward
	if totalCost != 0:
		ROI = round(diff / totalCost, 2)
	else:
		ROI = 0
		
	if ROI > best_ROI:
		best_fruit = fruit
		best_ROI = ROI
		
	print(f"{fruit}\t{upgrades}\t{ROI}\t{totalCost}\t{diff}")
print("best fruit to upgrade is " + str(best_fruit))



