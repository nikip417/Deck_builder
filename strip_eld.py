import json

def seperate(data):

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

def strip(data):
	cards = []
	unique_count = 0
	total_count = 0
	print(data['cards'][0])
	for card in data['cards']:
		text = ""
		if "text" in card:
			text =  card["text"]

		card_stripped = {
			"name": card["name"],
			"type": card["types"],
			"colors": card["colors"],
			"convertedManaCost": card["convertedManaCost"],
			"text": text,
			"count": 1
		}
		if card_stripped not in cards:
			cards.append(card_stripped)
			unique_count = unique_count + 1
		else: 
			print("we have a dupe!!!! - " + card_stripped["name"])

		total_count = total_count+1

	print("unique_count: " + str(unique_count))
	print("total_count: " + str(total_count))
	save_cards("ELD_STRIPPED.json", {"cards": cards})

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

	# seperate(data)
	strip(data)

	
		