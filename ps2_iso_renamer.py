import sys, os, re
titles = 'games.csv'
keepcharacters = (' ','.','_','-')

def gameTitleFromCSV(ID):
	with open(titles) as t:
		for line in t:
			if line.startswith(ID):
				return line.split(';')[1] # [0] = id, [1] = title
	
second_chars = [b'C', b'L'] # SCxS, SLxS
third_chars = [b'P', b'E', b'U'] # SxPS, SxES, SxUS
fourth_chars = [b'S', b'M']

for file in os.listdir('.'):
	if file.lower().endswith('iso'):
		string = ""
		with open(file, "rb") as f: # there is probably a *much* better way to do this
			byte = f.read(1)
			while byte:
				if byte == b'S' and string == "":
					string = byte.decode()
					byte = f.read(1)
					if byte in second_chars:
						string += byte.decode()
						byte = f.read(1)
						if byte in third_chars:
							string += byte.decode()
							byte = f.read(1)
							if byte in fourth_chars:
								string += byte.decode()
								byte = f.read(7)
								string += byte.decode()
								if "." in string:
									break
								else:
									string = ""
				else:
					string = ""

				byte = f.read(1)

		# clean up filename and get title from .csv
		gameID = string.replace('_', '-')
		gameID = gameID.replace('.', '')
		title = gameTitleFromCSV(gameID)
		cleanedTitle = "".join(c for c in title if c.isalnum() or c in keepcharacters).rstrip() # https://stackoverflow.com/a/7406369
		cleanedTitle = cleanedTitle.replace('  ', ' ')
		new_name = cleanedTitle + ' [' + gameID + '].iso'

		# rename
		print (file, '--->', new_name)
		os.rename(file, new_name)
