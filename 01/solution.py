with open('01/input.txt') as file:
    lines = file.readlines()

totals = []

for line in lines:
    if totals == []:
        totals.append(int(line))
    elif line.isspace():
        totals.append(0)
    else:
        totals[-1] += int(line)

topTotals = []
topFrequency = 3

for i in range(topFrequency):
    maxValue = max(totals)
    print("Top elf #{n} has {c} calories".format(n=i+1, c=maxValue))
    topTotals.append(maxValue)
    totals.remove(maxValue)

sumTopTotals = sum(topTotals)
print("Top {f} elves have a total of {c} calories".format(f=topFrequency, c=sumTopTotals))