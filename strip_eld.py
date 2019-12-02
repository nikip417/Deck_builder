import json

def strip(data):

	land_cards = []
	other_cards = []
	
	count=0
	for card_name in data['cards']:
		if 'Land' in card_name["types"]:
			land_cards.append(card_name)
		else:
			other_cards.append(card_name)
		count = count+1

	print(count)
	print("saving lands")
	save_cards("ELD_LANDS.json", land_cards)

	print("saving others")
	save_cards("ELD_OTHER.json", other_cards)
	return

def print_cards(cards_array):
	for card in cards_array:
		print(card["types"])

def save_cards(file_name, cards_array):

	with open(file_name,'w',encoding = 'utf=8') as write_file:
            json.dump(cards_array,write_file)



if __name__ == '__main__':
	filename = 'ELD.json'
	with open(filename,'r',encoding = 'utf=8') as read_file:
		data = json.load(read_file)

	strip(data)

	
		