# Useful MTG scripts
A collection of scripts and other useful things for your MTG collection

There are currently two Python scripts, one that imports your purchases from Cardmarket to Maxfield, and the other from Cardmarket to Archidekt. They are very similar, but outputs in the respective format for the two sites.

# Set-up:
1) You need to install the Python library Scrython (https://github.com/NandaScott/Scrython), from terminal: `pip install scrython` or `pip3 install scrython`
2) You probably need to install certificated in order to be able to make requests to the Scryfall API. Run the `Install Certificates.command` file within your Python install folder (at least it is like this on a Mac)
3) Save the Cardmarket page where you have your purchased cards as `input.html` in the same folder as the python scripts
4) Run the script, for example `python3 cardmarket_moxfield.py`
5) You'll get confirmation in the terminal if it found all sets etc.
6) Import the output.csv

Note: 
* The converter from set name to set code is far from perfect, and I've added some code to change certain set names from Cardmarket to the set names used in Scryfall, but there are for sure many more set names that needs to be changed in the same manner.
* Cards with 'token' in its name are removed from the csv.
* The (V.x) postfix from Cardmarket is removed
