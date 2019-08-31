import csv
import numpy as np

with open('banda_scan_time.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	line_count = 0
	mins=[]
	for row in csv_reader:
		if line_count == 0:
			print(f'Column names are {", ".join(row)}')	
		line_count += 1
		if 'BANDA' in row['BANDA_ID']:
			num = int(row['BANDA_ID'].replace("BANDA",""))
			elaps= row['ELAP_TIME'].split(":")
			if num <140  and int(elaps[0])>0:
				mins.append(int(elaps[0])*60+int(elaps[1]))

		line_count += 1
	print(np.mean(mins), np.std(mins))

	print(f'Processed {line_count} lines.')
