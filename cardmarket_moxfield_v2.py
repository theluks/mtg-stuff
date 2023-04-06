#import requests
import scrython
from bs4 import BeautifulSoup
import csv

cardno = 0
sets = scrython.sets.Sets()
setcode = 'none'

# Replace [set-name] with the name of the set you want to scrape
#url = 'https://www.cardmarket.com/en/Magic/Products/Singles/[set-name]'
#response = requests.get(url)

#Manually specify file
#inFile = open('input.html')
with open("input.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

#soup = BeautifulSoup(inFile, 'html.parser')

# Find all the cards on the page and extract their data
cards = soup.find_all("tr", "data-article-id"==True)
#print(cards)
card_data = []
for card in cards:
    cardno = cardno + 1
    #print(card)

    #Find card name
    if(card.has_attr('data-name')):
        card_name = card.attrs['data-name']
        if card_name.casefold().find('token') != -1:
            #Token found
            token = True
        else:
            token = False
        if card_name.casefold().find('(v.') != -1:
            #Version in name found, removing
            end = card_name.casefold().find('(v.')-1
            card_name = card_name[0:end]
    else:
        print("Cardname attribute not found") 
    #print(card_name)


    #Find quantity of cards
    if(card.has_attr('data-amount')):
        card_amount = card.attrs['data-amount']
        #print(card_amount)
    else:
        print("Amount of cards attribute not found")

    #Find set name
    if(card.has_attr('data-expansion-name')):
        card_set = card.attrs['data-expansion-name']
        if card_set.casefold().find('core') != -1:
            card_set = card_set[:5] + 'Set ' + card_set[5:]
            if card_set.casefold().find(': extras') != -1:
                #card_set = card_set.rstrip(card_set[-8])
                card_set = card_set[:-8]
        elif card_set.casefold().find('revised') != -1:
            card_set = 'Revised Edition'
        elif card_set.casefold().find('commander: innistrad: midnight hunt') != -1:
            card_set = 'Midnight Hunt Commander'
        elif card_set.casefold().find('retro frame artifacts') != -1:
            card_set = "The Brothers' War Retro Artifacts"
        elif card_set.casefold().find('commander: kamigawa: neon dynasty') != -1:
            card_set = 'Neon Dynasty Commander'
        elif card_set.casefold().find('commander: innistrad: crimson vow') != -1:
            card_set = 'Crimson Vow Commander'
        elif card_set.casefold().find('mystical archive') != -1:
            card_set = 'Strixhaven Mystical Archive'
        elif card_set.casefold().find('commander: strixhaven') != -1:
            card_set = 'Commander 2021'
        elif card_set.casefold().find('universes beyond: warhammer') != -1:
            card_set = 'Warhammer 40,000 Commander'
        elif card_set.casefold().find('commander: adventures in the forgotten') != -1:
            card_set = 'Forgotten Realms Commander'
        elif card_set.casefold().find('commander: streets of') != -1:
            card_set = 'New Capenna Commander'
        elif card_set[:12].casefold().find('commander 20') != -1:
            #Don't change setname here
            card_set = card_set
        elif card_set[:10].casefold().find('commander:') != -1:
            card_set = card_set[11:] + ' Commander'
        elif card_set.casefold().find(': extras') != -1:
            #setname = setname.rstrip(setname[-8])
            card_set = card_set[:-8]
        success = False
        for i in range(sets.data_length()):
            if sets.data(i, "name").casefold() == card_set.casefold():
                #print("Set code:", sets.data(i, "code"))
                setcode = sets.data(i, "code")
                success = True
                break
        if success == False:
            print("Error finding set: ", card_set, 'for card: '  + '"' + card_name + '"')
            setcode = 'MANUALINPUT'
    else:
        print("Could not find set name attribute")

    #Find quantity of cards
    if(card.has_attr('data-number')):
        card_collno = card.attrs['data-number']
    else:
        print("Collectors number attribute not found")

    #Find condition of card
    if(card.has_attr('data-condition')):
        card_condition = card.attrs['data-condition']
        match card_condition:
            case '1':
                card_condition = 'Mint'
            case '2':
                card_condition = 'Near Mint'
            case '3':
                card_condition = 'Lightly Played'
            case '4':
                card_condition = 'Played'
            case '5':
                card_condition = 'Played'
            case '6':
                card_condition = 'Heavily Played'
            case '7':
                card_condition = 'Damaged'
            case other:
                print('Error: Condition not found for card: ' + '"' + card_name + '"')
                card_condition = 'MANUALINPUT'
    else:
        print("Card condition attribute not found")

    #Find language of cards
    if(card.has_attr('data-language')):
        card_language = card.attrs['data-language']
        match card_language:
            case '1':
                card_language = 'English'
            case '4':
                card_language = 'Spanish'
            case '7':
                card_language = 'Japanese'
            case other:
                print('Error: Language not found for card: ' + '"' + card_name + '"')
                card_language = 'MANUALINPUT'
    else:
        print("Card language attribute not found")

    #Find foil of cards
    card_foil_soup = card.find(attrs={"title": "Foil"})
    #print(card_foil_soup)
    if card_foil_soup is not None:
        card_foil = card_foil_soup.attrs['title']
        #print(card_foil)
    else:
        card_foil = ''

    #Find price of card
    if(card.has_attr('data-price')):
        card_price = card.attrs['data-price']
        #print(card_price)
    else:
        print("Amount of cards attribute not found")

    # Create a dictionary to store the extracted data for each card
    if token == False:
        print('Writing card #', cardno, "to file")
        card_dict = {'Count': card_amount, 'Name': card_name, 'Edition': setcode, 'Condition': card_condition, 'Language': card_language, 'Foil': card_foil, 'Collector Number': card_collno}
        card_data.append(card_dict)
    else:
        print('Token found, "' + card_name + '", not writing to file')

#Write to csv file
with open('moxfield_data.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, delimiter=',',quoting=csv.QUOTE_ALL, fieldnames=['Count', 'Name', 'Edition', 'Condition', 'Language', 'Foil', 'Collector Number'])
    writer.writeheader()
    writer.writerows(card_data)