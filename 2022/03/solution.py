def getPriority(char):
    charCode = ord(char)
    if 64 < charCode < 91:
        return charCode - 38
    elif 96 < charCode < 123:
        return charCode - 96

def findSharedItems(compartments):
    sharedItems = []
    for compartment in compartments:
        for item in compartment:
            isSharedItem = True
            for otherCompartment in compartments:
                if compartment != otherCompartment and item not in otherCompartment:
                    isSharedItem = False
            if isSharedItem is True:
                sharedItems.append(item)
    return sharedItems


# Part 1: find priorities of shared items in rucksack compartments

with open('03/input.txt') as file:
    supplies = file.readlines()

sharedItemPrioritySum = 0
for rucksack in supplies:

    # Separate the compartments
    mid = int(len(rucksack)/2)
    compartment1 = rucksack[0:mid]
    compartment2 = rucksack[mid:]

    # Identify the shared item and get priority
    sharedItem = findSharedItems([compartment1, compartment2])[0]
    sharedItemPrioritySum += getPriority(sharedItem)

print("Shared Item Priority Sum: {}".format(sharedItemPrioritySum))

# Part 2: find priorities of badges in groups of three rucksacks

badgePrioritySum = 0
for group in range(int(len(supplies)/3)):

    # Identify the rucksacks in each group
    rucksack1 = supplies[group * 3]
    rucksack2 = supplies[group * 3 + 1]
    rucksack3 = supplies[group * 3 + 2]

    # Identify the badge item and get the item priority
    badge = findSharedItems([rucksack1, rucksack2, rucksack3])[0]
    badgePrioritySum += getPriority(badge)

print("Badge Priority Sum: {}".format(badgePrioritySum))