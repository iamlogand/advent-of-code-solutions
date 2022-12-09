with open('2/input.txt') as file:
    tournament = file.readlines()

outcomePairs = {
'draw': ['A A', 'B B', 'C C'],
'win':  ['A B', 'B C', 'C A'],
'lose': ['A C', 'B A', 'C B']
}

score = 0

for round in tournament:

    # Add score for outcome
    match round[2]:
        case 'X': outcome = 'lose'
        case 'Y': outcome = 'draw'; score += 3
        case 'Z': outcome = 'win'; score += 6

    # Find the matching pair of shapes that result in the required outcome
    # using list comprehension
    pair = [p for p in outcomePairs[outcome] if p[0] == round[0]][0]

    # Add score for my shape
    myShape = pair[2]
    match myShape:
        case 'A': score += 1
        case 'B': score += 2
        case 'C': score += 3

print("Total score: {}".format(score))