import math
from scipy.stats import norm


# --- CONSTANTS ---
amount_owned_cat = 0
amount_owned_bird = 0
amount_owned_dog = 0
amount_owned_lizard = 0
amount_owned_fish = 0

free_time_std = 2
furniture_percentage = 0.6
space_per_person = 20

space_need_cat = 2
space_need_bird = 1
space_need_dog = 7
space_need_lizard = 1
space_need_fish = 0.2

time_need_cat = 2
time_need_bird = 1
time_need_dog = 3
time_need_lizard = 1.5
time_need_fish = 1

money_need_cat = 1800
money_need_bird = 1200
money_need_dog = 2000
money_need_lizard = 2000
money_need_fish = 700

time_needed_already = amount_owned_cat*time_need_cat + amount_owned_bird*time_need_bird + amount_owned_dog*time_need_dog + amount_owned_lizard*time_need_lizard + amount_owned_fish*time_need_fish 
space_need_already = amount_owned_cat*space_need_cat + amount_owned_bird*space_need_bird + amount_owned_dog*space_need_dog + amount_owned_lizard*space_need_lizard + amount_owned_fish*space_need_fish 
money_needed_already = amount_owned_cat*money_need_cat + amount_owned_bird*money_need_bird + amount_owned_dog*money_need_dog + amount_owned_lizard*money_need_lizard + amount_owned_fish*money_need_fish


# --- THREE FUNCTIONS TO GET INDICES
def get_income_index(house_income, cost_of_living):
    income_steepness = 0.00005
    required_income = 1.2 * (cost_of_living + money_needed_already + money_need_cat)
    return 1 / (1 + math.exp(-income_steepness*(house_income-required_income)))

def get_time_index(owner_freetime):
    net_time = owner_freetime - time_needed_already
    z = (net_time - time_need_cat) / free_time_std
    return norm.cdf(z)

def get_space_index(population_density, people_in_household, floor_area, outside_area):
    human_space = furniture_percentage * floor_area + 10*math.log10(outside_area+1) - space_per_person*people_in_household - space_need_already - space_need_cat
    ratio = human_space / space_need_cat
    
    space_median = -0.00559007*population_density + 26.1558
    space_steepness = 0.0000275031*population_density + 0.0702201
    
    return 1/(1+math.exp(-space_steepness*(ratio-space_median)))
    



# --- GETTING THE HPFI ---
def get_HPFI(population_density, cost_of_living, household_income, people_in_household, owner_freetime, floor_area, outside_area):
    
    income_index = get_income_index(household_income, cost_of_living)
    time_index = get_time_index(owner_freetime)
    space_index = get_space_index(population_density, people_in_household, floor_area, outside_area)
    
    # print(income_index, time_index, space_index)
    
    return income_index ** (1/3) * time_index ** (1/3) * space_index ** (1/3)
 

if __name__ == '__main__':
    print(get_HPFI(4200, 89000, 120000, 2, 5, 80, 5))

