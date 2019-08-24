import sys, os
titles = 'ps2_ids.txt'
keepcharacters = (' ','.','_','-') # Characters to keep when cleaning up the filename

def gameTitleFromCSV(ID):
	with open(titles) as t:
		for line in t:
			if ID in line:
				return line.split(';')[0] # [0] = title, [1] = id's

for file in os.listdir('.'):
	if file.lower().endswith('iso'):
		#print (file)
		bytelist = []
		with open(file, "rb") as f:
			byte = f.read(1)
			while byte:
				
				bytelist.append(byte)
				if len(bytelist) == 11:  # SLPS-205.33 = 11 bytes 
					if ord(bytelist[4]) == 95 and ord(bytelist[8]) == 46: # 5 char is _ and 9th is . (ascii)
					#TODO: probably do more sanity checking to make sure first 4 chars are alpha etc
						try:
							string = b''.join(bytelist).decode('utf8')
							#print (string)
							break
						except UnicodeDecodeError:
							continue
					bytelist.pop(0) # remove first byte

				byte = f.read(1)

		# clean up filename and get title from .csv
		gameID = string.replace('_', '-') # these two lines converts SLUS_200.66 to SLUS-20066
		gameID = gameID.replace('.', '')
		title = gameTitleFromCSV(gameID)
		if not title: # if title is not in the csv
			print ('did not find title for', gameID, ' -- using filename instead')
			new_name = os.path.splitext(file)[0] + ' [' + gameID + '].iso'
		else:
			cleanedTitle = "".join(c for c in title if c.isalnum() or c in keepcharacters).rstrip() # https://stackoverflow.com/a/7406369
			cleanedTitle = cleanedTitle.replace('  ', ' ')
			new_name = cleanedTitle + ' [' + gameID + '].iso'

		# rename
		print (file, '--->', new_name)
		os.rename(file, new_name)