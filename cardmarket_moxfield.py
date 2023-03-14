#https://github.com/NandaScott/Scrython
import scrython

#Creates a file from Cardmarket html for import at Archidekt

inFile = open('input.html')
outFile = open('output.csv', 'w')
string = inFile.readline()
#first product index    
index = string.find("data-product-id")
cardno = 0
sets = scrython.sets.Sets()
setcode = 'none'

#write csv header:
outFile.write('"Count"' + ',' + '"Name"' + ',' + '"Edition"' + ',' + '"Condition"' + ',' + '"Language"' + ',' + '"Foil"' + ',' + '"Collector Number"' + '\n')

while index != -1:
    cardno = cardno + 1
    #finding next Product ID
    #index = string.find("data-product-id")

    #Quantity of cards
    sub_index = string.find('data-amount', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    quantity = string[start:end]
    #outFile.write(string[start:end] + ',')

    #Card name
    sub_index = string.find('data-name', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    name = string[start:end]
    if name.casefold().find('token') != -1:
        #Token found
        token = True
    else:
        token = False
    if name.casefold().find('(v.') != -1:
        #Version in name found, removing
        end = name.casefold().find('(v.')-1
        name = name[0:end]
    #outFile.write(string[start:end] + ',')

    #find set code
    sub_index = string.find('data-expansion-name', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    setname = string[start:end]
    #making some set name adjustments to suit Scryfall
    if setname.casefold().find('core') != -1:
        setname = setname[:5] + 'Set ' + setname[5:]
        if setname.casefold().find(': extras') != -1:
            #setname = setname.rstrip(setname[-8])
            setname = setname[:-8]
    elif setname.casefold().find('commander: innistrad: midnight hunt') != -1:
        setname = 'Midnight Hunt Commander'
    elif setname.casefold().find('retro frame artifacts') != -1:
        setname = "The Brothers' War Retro Artifacts"
    elif setname.casefold().find('commander: kamigawa: neon dynasty') != -1:
        setname = 'Neon Dynasty Commander'
    elif setname.casefold().find('mystical archive') != -1:
        setname = 'Strixhaven Mystical Archive'
    elif setname.casefold().find('commander: strixhaven') != -1:
        setname = 'Commander 2021'
    elif setname.casefold().find('universes beyond: warhammer') != -1:
        setname = 'Warhammer 40,000 Commander'
    elif setname.casefold().find('commander: adventures in the forgotten') != -1:
        setname = 'Forgotten Realms Commander'
    elif setname.casefold().find('commander: streets of') != -1:
        setname = 'New Capenna Commander'
    elif setname[:12].casefold().find('commander 20') != -1:
        #Don't change setname here
        setname = setname
        #print (setname)
    elif setname[:10].casefold().find('commander:') != -1:
        setname = setname[11:] + ' Commander'
        #print (setname)
    elif setname.casefold().find(': extras') != -1:
        #setname = setname.rstrip(setname[-8])
        setname = setname[:-8]
        #print (setname)
    success = False
    for i in range(sets.data_length()):
        if sets.data(i, "name").casefold() == setname.casefold():
            #print("Set code:", sets.data(i, "code").upper())
            setcode = sets.data(i, "code")
            success = True
            break
    if success == False:
        print("Error finding set: ", setname, 'for card: '  + '"' + name + '"')
        setcode = 'MANUALINPUT'

    #Collection number
    sub_index = string.find('data-number', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    collnumber = string[start:end]

    #Condition
    sub_index = string.find('data-condition', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    condition = string[start:end]
    match condition:
        case '1':
            condition = 'NM'
        case '2':
            condition = 'NM'
        case '3':
            condition = 'LP'
        case '4':
            condition = 'MP'
        case '5':
            condition = 'MP'
        case '6':
            condition = 'HP'
        case '7':
            condition = 'D'
        case other:
            print('Error: Condition not found for card: ' + '"' + name + '"')
            condition = 'MANUALINPUT'

    #Language on card
    sub_index = string.find('data-language', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    language = string[start:end]
    match language:
        case '1':
            language = 'English'
        case '4':
            language = 'Spanish'
        case '7':
            language = 'Japanese'
        case other:
            print('Error: Language not found for card: ' + '"' + name + '"')
            language = 'MANUALINPUT'

    #Foil
    #move index to extras column
    index = string.find('col-extras', index)
    sub_index = string.find('title', index)
    start = string.find('"', sub_index)+1
    end = string.find('"', start)
    foil = string[start:end]
    if foil != 'Foil':
        foil = ''
    else:
        foil = 'foil'

    #Price
    #index = string.find('data-price', index)
    #start = string.find('"', index)+1
    #end = string.find('"', start)
    #price = string[start:end]

    #write to file if nontoken
    if token == False:
        print('Writing card #', cardno, "to file")
        outFile.write('"' + quantity + '","' + name + '","' + setcode + '","' + condition + '","' + language + '","' + foil + '","' + collnumber + '"\n')
    else:
        print('Token found, "' + name + '", not writing to file')

    #move index to next item
    index = string.find('data-article-id', index)