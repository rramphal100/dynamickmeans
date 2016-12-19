with open("dow_jones_index.data", "r") as infile:
	with open("data.csv", "w") as outfile:
		for line in infile:
			linearray = line.split(",")
			if "" not in linearray:
				outfile.write(line)