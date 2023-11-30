with open('02/input.txt') as file:
    tournament = file.readlines()

score = 0

for round in tournament:
    
    outcome = ''

    match round[2]:

        case 'X':  # I play rock
            score += 1

            match round[0]:
                case 'C':  # Opponent plays scissors
                    outcome = 'win'
                case 'A':  # Opponent plays rock
                    outcome = 'draw'

        case 'Y':  # I play paper
            score += 2

            match round[0]:
                case 'A':  # Opponent plays rock
                    outcome = 'win'
                case 'B':  # Opponent plays paper
                    outcome = 'draw'

        case 'Z':  # I play scissors
            score += 3

            match round[0]:
                case 'B':  # Opponent plays paper
                    outcome = 'win'
                case 'C':  # Opponent plays scissors
                    outcome = 'draw'

    if outcome == 'win':
        score += 6
    elif outcome == 'draw':
        score += 3

print("Total score: {}".format(score))