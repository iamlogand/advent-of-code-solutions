import re


def getSetOfIds(bounds):
    splitBounds = re.split("-", bounds)
    sectionIds = []
    for id in range(int(splitBounds[0]), int(splitBounds[1]) + 1):
        sectionIds.append(id)
    return set(sectionIds)


with open('2022/04/input.txt') as file:
    assignments = file.readlines()

containingPairCount = 0
overlappingPairCount = 0
for pair in assignments:

    # Get a set of section IDs for each elf
    splitPair = re.split(",", pair)
    firstSet = getSetOfIds(splitPair[0])
    secondSet = getSetOfIds(splitPair[1])

    # Check if one section is a subset of the other
    if firstSet.issubset(secondSet) or secondSet.issubset(firstSet):
        containingPairCount += 1

    # Check if one sections overlaps the other
    if firstSet.intersection(secondSet):
        overlappingPairCount += 1

print("Pairs in which one section completely contains the other: {}".format(containingPairCount))
print("Pairs in which sections overlap: {}".format(overlappingPairCount))