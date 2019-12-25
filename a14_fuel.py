from pprint import pprint
import copy

data = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

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
need['FUEL'] = 1

def deconstruct(chem):
    '''Adjust the ingredient list assuming we've made one recipie of <chem>'''
    global need
    global make
    if chem in need and need[chem] > 0:
        for ingredient_chem, ingredient_quant in make[chem].items():
            if ingredient_chem == chem:
                need[chem] -= ingredient_quant
            else:
                need[ingredient_chem] += ingredient_quant

def deconstruct_everything():
    '''Adjust the ingredient list until all we need is ORE.'''
    global need
    while [chem for chem in need if need[chem] > 0 and chem != 'ORE']:
        for chem in need:
            if chem == 'ORE':
                continue
            if need[chem] > 0:
                deconstruct(chem)

deconstruct_everything()
print(f'To make 1 FUEL we need {need["ORE"]} ORE.')
# print(f'And have this extra stuff:')
# print({c:abs(i) for c, i in need.items() if i < 0})



        
