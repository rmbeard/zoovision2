import locale as LOCALE

fo = open("weights.txt", "r")
fw = open("weights.gwt", "w")
header = fo.readline()
fw.write("%s" % header)
data = fo.readlines()
for row in data:
    rowVals = row.split()
    rowID = rowVals[0]
    weights = rowVals[1:]
    for colID, weight in enumerate(weights):
        w = LOCALE.atof(weight)
        if w != 0.0:
            fw.write("%s %i %s\n" % (rowID, colID + 1, weight))

fo.close()
fw.close()
