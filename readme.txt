The program was coded and tested using python 3.6 on Ubuntu 18.04 LTS.

Files needed to run the program:
	deckbuilder_ga_final.py
	ELD.json (or other json formated card file from mtgjson.com)    # the program can use other files by passing the filename
																	# to line 56, loadjson('enter_filename_here')

Optional files:
	booster_pool_picked	    # this file is used to load a saved booster pool instead of generating a random one each time the 		                    # program is executed. Change line 254 generate_booster_pool('option') parameter to anything but 								# 'new'

Place them in the same directory.
	Open a terminal session, set the current directory to the one containing the files.
	Execute the program using ./deckbuilder_ga_final.py


CONSTANTS that can be changed by a user:
	DECK_POOL_SIZE = 6 * 15  # can change the first number to represent the number of booster packs to use for sealed deck play
	DECK_SIZE = 40  		 # can be changed to any number the user would like, but must be less than DECK_POOL_SIZE
	NUM_DECKS = 20  		 # of random decks to build, must be even number
	MUTATE_ODDS = 0.1		 # changes the probability of mutating a member of the population
	GENERATION_LIMIT = 5000	 # how many times to loop through the ga


Program Outputs:
	The program generates a json file of each deck from the first generation as well as the last generation, for a total of 40 decks.  These files are located in the same directory as the program.  The file names are deckX_Ypop.json, where X is the deck number, and Y either 'initial' or 'final'.

	It outputs the average fitness history of each generation in a file called 'fitness_history.txt'.

	It outputs the deck statistics from every deck created in a file called 'deck_stats.txt'.  This file follows the data structure d = {'deckno':deck_uid,'deckcolor':[],'cards':[],'fitness':0,'evasioncount':0,'creaturecount':0,'spellcount':0,\
             'bombcount':0,'landcount':0}.  This is a dictionary that is used by the fitness function to calculate the various measures of fitness.  It omits the 'cards' key and values for readability purposes.
