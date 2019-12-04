#!/usr/bin/python3

import time,random,statistics,json,pickle,os

# CONSTANTS
GOAL = 17  # set to the total number of points possible in fitness function
DECK_POOL_SIZE = 6 * 15  #need to increase to ensure filtered set has enough cards of each color for populate function
DECK_SIZE = 90
NUM_DECKS = 50 # of random decks to build, must be even number
MUTATE_ODDS = 0.1
GENERATION_LIMIT = 25

def save(dObj,sFilename):
    # Given an object and a file name, write the object to the file using pickle.
    f = open(sFilename,"wb")
    p = pickle.Pickler(f)
    p.dump(dObj)
    f.close()

def load(sFilename):
    # Given a file name, load and return the object stored in the file.
    f = open(sFilename,"rb")
    u = pickle.Unpickler(f)
    dObj = u.load()
    f.close()
    return dObj

def load_json(filename = 'ELD.json'):
    # read in the json data, parse into python list

    with open(filename,'r',encoding = 'utf=8') as read_file:
        data = json.load(read_file)

    all_cards = []
    for card_name in data['cards']:
        all_cards.append(card_name)
    # print(len(all_cards), 'cards loaded')
    return all_cards

def save_forge_data(data):
    try:
        os.mkdir("forge_data")
    except:
        print("forge_data directory exists")
    os.chdir("forge_data")

    # save the data in the necessary format
    i = 0
    while i < NUM_DECKS:
        fname = 'deck' + str(i + 1) + '_' + "final_pop_forge.json"
        deck = data[i]
        with open(fname,'w',encoding = 'utf=8') as write_file:
            for card in deck['cards']:
                string = json.dumps(card['name']).replace('"', '')
                write_file.write(string)
                write_file.write('\n')
        i += 1
    os.chdir("..")

def save_json(filename,data):
    # write the json data
    try:
        os.mkdir("decks")
    except:
        print("decks directory exists")
    os.chdir("decks")

    if filename == "final_pop.json":
        # put the data in a format forge can recognize
        save_forge_data(data)

    # write the json data
    i = 0
    while i < NUM_DECKS:
        fname = 'deck' + str(i + 1) + '_' + filename
        deck = data[i]
        # print(len(deck['cards']),'cards saved in deck ',i+1)
        with open(fname,'w',encoding = 'utf=8') as write_file:
            json.dump(deck['cards'],write_file)
        i += 1
    os.chdir("..")

def generate_booster_pool(option):
    '''Randomly build a pool of cards. Logic prevents pool from containing the same card twice.'''
    booster_pool = []
    picked_cards = []
    if str(option).lower() == 'new':
        cs = load_json()    #pass a filename to load_json() function to use a different card set
        t = 0
        while t < DECK_POOL_SIZE:
            i = random.randint(0,len(cs))
            if cs[i - 1] not in picked_cards:
                booster_pool.append(cs[i - 1])
                picked_cards.append(cs[i - 1])
                t += 1
        save(booster_pool,'booster_pool_pickled')
    else:
        try:
            booster_pool = load('booster_pool_pickled')
        except:
            print('File not found')

    return booster_pool

def color_sets(set):
    #TODO - not implemented, but possible improvement to force deck color combos
    deck_color = ['W','B','G','U','R','']
    filtered_set = []
    for c in deck_color:
        d = {'deckcolor':c,'cards':[]}
        for card in set:
            if c in card['colorIdentity']:
                d['cards'].append(card)
                #print_card(card)
        filtered_set.append(d)

    t = 0
    for f in filtered_set:
        print(len(f['cards']))
        t += len(f['cards'])
    print('total cards filtered: ',t)

    return filtered_set

def populate(cardpool):
    """Create an initial population of decks."""
    init_pop = []
    #deck_color = ['W','B','G','U','R','']
    for i in range(1,NUM_DECKS + 1):
        ''' "d" establishes the data structure of the deck.  The fitness function
            will modify the "fitness' key value to something other than zero.
            this will then be used to cull the population to eliminate the weakest
        '''
        d = {'deckno':i,'deckcolor':[],'cards':[],'fitness':0,'evasioncount':0,'creaturecount':0,'spellcount':0,\
             'bombcount':0,'landcount':0}
        # TODO - add logic to make smarter decks:
        # 1. make a deck based on color - need to add additional dic key 'deckcolor'
        # 2. have a ratio of creatures - instants/enchantments
        picked_cards = []
        j = 0
        while j < DECK_SIZE:
            n = random.randint(0,len(cardpool) - 1)
            card = cardpool[n - 1]
            if card not in picked_cards:
                d['cards'].append(card)
                picked_cards.append(card)
                #print_card(card)
                j += 1
        init_pop.append(d)

    save_json('initialpop.json',init_pop)
    return init_pop

def fitness(deck,deck_hist):
    """Measure fitness of a deck based on a target."""
    ave_fitness = 0
    for d in deck:
        #reinitialize counts
        d['fitness'] = 0
        d['creaturecount'] = 0
        d['spellcount'] = 0
        d['evasioncount'] = 0
        d['bombcount'] = 0
        d['landcount'] = 0
        #perform counts of key features
        for card in d['cards']:
            for color in card['colors']:
                if color not in d['deckcolor']:
                    d['deckcolor'].append(color)
            if 'Land' in card['type']:
                d['landcount'] += 1
            elif 'Creature' in card['type']:
                if card['convertedManaCost'] > 5:
                    d['bombcount'] += 1
                else:
                    d['creaturecount'] += 1
            elif 'Spell' in card['type'] or 'Instant' in card['type'] or 'Enchantment' in card['type'] or 'Artifact' in\
                    card['type'] or 'Sorcery' in card['type']:
                d['spellcount'] += 1
            if 'text' in card:
                if 'flying' in card['text'] or 'menace' in card['text'] or 'first strike' in card['text'] or 'trample' \
                        in card['text']:
                    d['evasioncount'] += 1

        #calculate fitness of deck
        # Checks for conformance to B.R.E.A.D
        # 1. check for diversity of deck colors, higher diversity should be rated lower (6 possible points)
        if len(d['deckcolor']) == 1:
            d['fitness'] += 4
        elif len(d['deckcolor']) == 3:
            d['fitness'] += 5
        elif len(d['deckcolor']) == 2:
            d['fitness'] += 6
        # 2. check for appropriate creature/mana curve (2 possible points)
        if d['creaturecount'] >= 3 and  d['creaturecount'] >= 5:
            d['fitness'] += 2
        elif d['creaturecount'] == 2 or d['creaturecount'] == 4:
            d['fitness'] += 1
        # 3. Evasion - check for certain creature abilities, flying, trample, etc. (3 possible points)
        if d['evasioncount'] >= 6:
            d['fitness'] += 3
        elif d['evasioncount'] < 6 and d['evasioncount'] >= 3:
            d['fitness'] += 2
        elif d['evasioncount'] < 3 and d['evasioncount'] >= 1:
            d['fitness'] += 1
        # 4. have a ratio of creatures - instants/enchantments (2 possible points)
        if d['creaturecount'] > 0 and d['spellcount'] > 0:
            if d['creaturecount']/d['spellcount'] >= 0.8 and d['creaturecount']/d['spellcount'] <= 1.2:
                d['fitness'] += 2
            elif d['creaturecount']/d['spellcount'] >= 0.5 and d['creaturecount']/d['spellcount'] <= 1.5:
                d['fitness'] += 1
        # 5. bombs (4 possible point)
        if d['bombcount'] == 2:
            d['fitness'] += 4
        elif d['bombcount'] == 1:
            d['fitness'] += 3

        deck_hist.append('Deck no: '+str(d['deckno'])+' Colors: '+str(d['deckcolor'])+' Fitness: '+str(d['fitness'])\
                         +' No. Evasions: '+str(d['evasioncount'])+' No. Creatures: '+str(d['creaturecount'])\
                         +' No. Spells: '+str(d['spellcount'])+' No. Bombs '+str(d['bombcount'])+' No. Lands: '\
                         +str(d['landcount']))
        ave_fitness += d['fitness']
    ave_fitness = round(ave_fitness / len(deck), 3)
    return ave_fitness, deck_hist

def breed(deck_group_a,deck_group_b,deck_size,deck_uid):
    """Crossover genes among members of a population."""
    random.shuffle(deck_group_a)
    random.shuffle(deck_group_b)
    children = []
    for decka,deckb in zip(deck_group_a,deck_group_b):
        deck_uid += 1
        d = {'deckno':deck_uid,'deckcolor':[],'cards':[],'fitness':0,'evasioncount':0,'creaturecount':0,'spellcount':0,\
             'bombcount':0,'landcount':0}
        for child in range(deck_size // 2):
            carda = decka['cards'][random.randint(0,len(decka) - 1)]
            cardb = deckb['cards'][random.randint(0,len(deckb) - 1)]
            d['cards'].append(carda)
            d['cards'].append(cardb)
        children.append(d)
    return children,deck_uid

def cull(population,to_retain):
    """Cull a population to keep only the fittest members."""
    sorted_population = sorted(population,key = lambda i:i['fitness'],reverse = True)
    to_retain_by_group = to_retain // 2
    culled_pop = sorted_population[:to_retain]
    selected_group_a = culled_pop[:to_retain_by_group]
    selected_group_b = culled_pop[to_retain_by_group:]
    '''
    print("\nSorted Population, pop: ", len(sorted_population))
    for s in sorted_population:
        print("Deck Number: ", s['deckno'], ' Fitness Level: ', s['fitness'])
    '''
    return selected_group_a,selected_group_b

def mutate(population,boosterpool,mutate_odds):
    """Randomly swap a card in a given deck with one from the booster pool."""
    # add logic to maintain color diversity
    for i in population:
        n = random.uniform(0,1)
        # print(n)
        if mutate_odds >= n:
            card_from_deck = random.randint(0,len(i['cards']) - 1)
            new_card = random.randint(0,len(boosterpool) - 1)
            # print("Card before mutate: ", i['cards'][card_from_deck])
            i['cards'][card_from_deck] = boosterpool[
                new_card]  # print("Deck after mutate: ", i['cards'][card_from_deck])
    return population

def print_card(card):
    print('\n=== Card Info ===')
    print('Name: ',card['name'])
    print('colorIdentity:',card['colorIdentity'])
    print('Type-subtype: ',card['type'])
    if 'manaCost' in card and 'convertedManaCost' in card:
        print('manaCost: ',card['manaCost'])
        print('convertedManaCost: ',card['convertedManaCost'])
    if 'power' in card and 'toughness' in card:
        print('power/toughness: ',card['power'],'/', card['toughness'])
    if 'text' in card:
        print('text: ', card['text'])

def main():
    fitness_history = []
    generation = 0
    bp = generate_booster_pool('new')  # change to anything but new to force loading a pickle file
    parents = populate(bp)
    deck_stats =[]
    pop_fitness, deck_stats = fitness(parents, deck_stats)
    fitness_history.append(pop_fitness)
    deck_counter = len(parents)

    while pop_fitness < GOAL and generation < GENERATION_LIMIT:
        group_a, group_b = cull(parents, NUM_DECKS)
        children, deck_counter = breed(group_a, group_b, DECK_SIZE, deck_counter)
        parents = group_a + group_b + children
        mutate(parents, bp, MUTATE_ODDS)
        pop_fitness,deck_stats = fitness(parents, deck_stats)
        fitness_history.append(pop_fitness)
        generation += 1

    # print statistics
    if generation == GENERATION_LIMIT:
        print("\n=== Generation Limit Reached ===\n")
    elif pop_fitness == GOAL:
        print("\n=== Goal Reached ===\n")
    save_json('final_pop.json',parents)
    print("\nFitness by generation :")
    with open('fitness_history.txt', 'w') as fitness_file:
        for f in range(0, len(fitness_history)):
            fitness_file.write('Generation: '+str(f)+': Average population fitness: '+str(fitness_history[f])+'\n')
            print('Generation:', f, ' Average population fitness: ', fitness_history[f])
    fitness_file.close()
    print('\nDeck Statistics')
    with open('deck_stats.txt', 'w') as stats_file:
        for d in deck_stats:
            stats_file.write('%s\n' % d)
            print(d)
    stats_file.close()

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {} seconds.".format(duration))
