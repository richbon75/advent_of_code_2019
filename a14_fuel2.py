from pprint import pprint
import copy

with open('a14_input.txt','r') as f:
  data=f.read()

make = dict()
'''
ex: 1 A, 4 B => 1 AB   becomes:
    make['AB'] = {'AB':1, 'A':3, 'B':4}
'''
need = {'ORE':0}  # How much of which chemicals do we need?

for line in data.splitlines():
    ingredients, result = line.split('=>')
    result_quant, result_chem = result.strip().split(' ')
    result_quant = int(result_quant)
    make[result_chem] = {result_chem: result_quant}
    need[result_chem] = 0
    for ingredient in ingredients.strip().split(','):
        ingredient_quant, ingredient_chem = ingredient.strip().split(' ')
        make[result_chem][ingredient_chem] = int(ingredient_quant)

need_backup = copy.copy(need)

def deconstruct_max(chem):
    '''Adjust the ingredient list assuming we've made the max needed recipies of <chem>'''
    global need
    global make
    if chem in need and need[chem] > 0:
        makes_quant = make[chem][chem]
        quant_needed = need[chem]
        recipies_needed = quant_needed // makes_quant
        if quant_needed % makes_quant:
            recipies_needed += 1
        for ingredient_chem, ingredient_quant in make[chem].items():
            if ingredient_chem == chem:
                need[chem] -= ingredient_quant * recipies_needed
            else:
                need[ingredient_chem] += ingredient_quant * recipies_needed

def deconstruct_everything():
    '''Adjust the ingredient list until all we need is ORE.'''
    global need
    while [chem for chem in need if need[chem] > 0 and chem != 'ORE']:
        for chem in need:
            if chem == 'ORE':
                continue
            if need[chem] > 0:
                deconstruct_max(chem)

def ore_for_fuel(fuel):
    '''How much ore does it take to make this amount of fuel?'''
    global need
    global need_backup
    need = copy.copy(need_backup)
    need['FUEL'] = fuel
    deconstruct_everything()
    return need['ORE']

t = 1000000000000
# Binary search to find the amount of fuel that can be produced
# by 1 Trillion ORE.
fuel_min = 0
fuel_max = t
try_ore = 0
while fuel_min < fuel_max-1 and try_ore != t:
    try_fuel = (fuel_max + fuel_min) // 2
    try_ore = ore_for_fuel(try_fuel)
    if try_ore > t:
        fuel_max = try_fuel
    else:
        fuel_min = try_fuel
    print(fuel_min, fuel_max)
   
print(f'1 Trillion Ore can produde {fuel_min} fuel.')

