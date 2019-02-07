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
						  11:1,#Not verified
						  12:1,#Not verified
						  13:1}#Not verified
First_Harvest_Perk_Levels = 5
Seed_Reward_Perk_Levels = 10
Seed_Reward_Quirks_Levels = 25
#Equipment_Seed_Reward = 142.94 #%
#Equipment_Yeild_Reward = 10 #%
#NGU_Seed_Reward = 940.58 #%

Equipment_Seed_Reward = 28.2 #%
Equipment_Yeild_Reward = 0 #%		OLD
NGU_Seed_Reward = 827.19 #%



#TODO påverkar Equipment_Yeild_Reward någon av seed rewardsen?
def get_seed_reward(fruit, tier, harvest = False, first_Harvest = False, poop = False):
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

	
	
#print(str(get_seed_reward(10, 2, False, True, False)))
print(str(get_eat_reward(1, 24, True, False) * 7.272e27 * 60))