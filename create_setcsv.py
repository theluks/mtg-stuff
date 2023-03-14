import scrython
outFile = open('setnames.csv', 'w')
sets = scrython.sets.Sets()
#write header
outFile.write('name' + ',' + 'code' + '\n')

for i in range(sets.data_length()):
	outFile.write(sets.data(i, "name") + ',')
	outFile.write(sets.data(i, "code").upper() + '\n')
	print("Set name:", sets.data(i, "name"))
	print("Set code:", sets.data(i, "code").upper())