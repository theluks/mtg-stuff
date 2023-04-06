# Useful MTG scripts
A collection of scripts and other useful things for your MTG collection

There are currently two Python scripts, one that imports your purchases from Cardmarket to Moxfield, and the other from Cardmarket to Archidekt. They are very similar, but outputs in the respective format for the two sites.

There are now two variants of the scripts, with the "v2" version using BeautifulSoup to extract the data, and a bit neater way to write to the csv files. 

# Set-up:
1) You need to install the Python library BeautifulSoup4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/), from terminal: `pip install beautifulsoup4` or `pip3 install beautifulsoup4`
2) You need to install the Python library Scrython (https://github.com/NandaScott/Scrython), from terminal: `pip install scrython` or `pip3 install scrython`
3) You probably need to install certificates in order to be able to make requests to the Scryfall API. Run the `Install Certificates.command` file within your Python install folder (at least it is like this on a Mac)
4) Save the Cardmarket page where you have your purchased cards as `input.html` in the same folder as the python scripts
5) Run the script, for example `python3 cardmarket_moxfield.py`
6) You'll get confirmation in the terminal if it found all sets etc.
7) Import the output.csv

Note: 
* The converter from set name to set code is far from perfect, and I've added some code to change certain set names from Cardmarket to the set names used in Scryfall, but there are for sure many more set names that needs to be changed in the same manner.
* Cards with 'token' in its name are removed from the csv.
* If something, like a setcode, is not found, it will appear as 'MANUALINPUT' in the csv to be manually edited before import.
* The (V.x) postfix from Cardmarket is removed
