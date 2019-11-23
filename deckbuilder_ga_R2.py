#!/usr/bin/python3

import time
import random
import statistics
import json

# CONSTANTS
GOAL = 50000  # need to determine some goal to test the fitness level against
DECK_POOL_SIZE = 90
DECK_SIZE = 40
NUM_DECKS = 20  # of random decks to build, must be even number
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
GENERATION_LIMIT = 500

def load_dataset():
    #read in the json data, parse into python list
    filename = 'ELD.json'
    with open(filename, 'r', encoding='utf=8') as read_file:
        data = json.load(read_file)

    all_cards = []
    for card_name in data['cards']:
        all_cards.append(card_name)
    print(len(all_cards), 'cards loaded')
    return all_cards

def generate_booster_pool(card_pool):
    '''Randomly build a pool of cards
    create list to hold hashtable of cards
    limit size to deck_pool_size
    '''
    t=0
    booster_pool=[]
    while t < DECK_POOL_SIZE:
        i=random.randint(0,len(card_pool))
        booster_pool.append(card_pool[i-1])
        t += 1
    return booster_pool

def populate(num_decks=NUM_DECKS):
    """Create an initial population of decks."""
    cs = load_dataset()
    bp = generate_booster_pool(cs)
    init_pop = []
    # ensure even-number of decks for breeding pairs:
    if num_decks % 2 == 0:
        num_decks += 1
    for i in range(1, num_decks):
        ''' "d" establishes the data structure of the deck.  The fitness function
            will modify the "fitness' key value to something other than zero.
            this will then be used to cull the population to eliminate the weakest
        '''
        d = {'deckno': i, 'cards':[], 'fitness':0}
        for j in range(DECK_SIZE):
            n = random.randint(0,len(bp))
            d['cards'].append(bp[n-1])
        init_pop.append(d)
    return init_pop

def fitness(deck):
    """Measure fitness of a deck based on a target."""
    for d in deck:
        #TODO - add fitness checks here, replace random assignment with real calculated value
        d['fitness'] = random.randint(1,5)

def breed(deck_group_a, deck_group_b, deck_size, deck_uid):
    """Crossover genes among members of a population."""
    random.shuffle(deck_group_a)
    random.shuffle(deck_group_b)
    children = []
    for decka, deckb in zip(deck_group_a, deck_group_b):
        deck_uid += 1
        d = {'deckno': deck_uid, 'cards': [], 'fitness': 0}
        for child in range(deck_size//2):
            d['cards'].append(decka['cards'][random.randint(0,len(decka)-1)])
            d['cards'].append(deckb['cards'][random.randint(0, len(deckb) - 1)])
        children.append(d)
    return children, deck_uid

def cull(population, to_retain):
    """Cull a population to keep only the fittest members."""
    sorted_population = sorted(population, key=lambda i: i['fitness'], reverse=True)
    to_retain_by_group = to_retain // 2
    members_per_group = len(sorted_population) // 2
    deck_group_a = sorted_population[:members_per_group]
    deck_group_b = sorted_population[members_per_group:]
    selected_group_a = deck_group_a[-to_retain_by_group:]
    selected_group_b = deck_group_b[-to_retain_by_group:]
    return selected_group_a, selected_group_b

def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Randomly swap a card in a given deck with one from the booster pool."""
    #TDDO - complete this function
    for index, card in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(card * random.uniform(mutate_min, mutate_max))
    return children

def print_card(card):
    print('\n=== Card Info ===')
    print('Name: ', card['name'])
    print('colorIdentity:', card['colorIdentity'])
    print('Type-subtype: ', card['type'])
    if 'Land' not in card['type']:
        print('manaCost: ', card['manaCost'])
        print('convertedManaCost: ', card['convertedManaCost'])
    if 'Creature' in card['type']:
        print('power/toughness: ', card['power'], '/', card['toughness'])
    if 'text' not in card:
        card['text'] = ""
    print('text: ', card['text'])

'''
def main():
    """Initialize population, select, breed, and mutate, display results."""
    generations = 0

    parents = populate(NUM_DECKS, DECK_SIZE, DECK_POOL_SIZE)
    popl_fitness = fitness(parents, GOAL)
    print("initial population fitness = {}".format(popl_fitness))
    print("number to retain = {}".format(NUM_DECKS))

    fitness_level = []

    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_a, selected_b = select(parents, NUM_DECKS)
        children = breed(selected_a, selected_b, DECK_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_a + selected_b + children
        popl_fitness = fitness(parents, GOAL)
        print("Generation {} fitness = {:.4f}".format(generations, popl_fitness))
        fitness_level.append(int(statistics.mean(parents)))
        generations += 1

    print("fitness level per generation = {}".format(fitness_level))
    print("\nnumber of generations = {}".format(generations))
'''
def main():
    init_pop = populate()
    print('initial population ', len(init_pop))
    for n in init_pop[0]['cards']:
        print_card(n)
    fitness(init_pop)
    for i in init_pop:
        print(i['deckno'], i['fitness'])
    group_a, group_b = cull(init_pop, NUM_DECKS)
    deck_counter = len(init_pop)
    children, deck_counter=breed(group_a, group_b, DECK_SIZE, deck_counter)
    parents = group_a + group_b + children
    print(len(parents))


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds.".format(duration))
