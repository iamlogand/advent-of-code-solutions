"""
THE PLAN

To find the route with the least heat loss, from the top left to the bottom right,
I'll have to calculate many possible paths from the start to the end, which is a lot of paths.

To save time when finding paths, I'll have to use dynamic programming, like problem 12.
The sub-problems needs to be framed in a repeatable way - by making a function that will be called many times with the same arguments.
The DP function results must be cached so that the results can be reused.

The sub-problem is finding the optimum route to the end given:
    - the starting location
    - the starting direction

So for the real input, the maximum number of sub-problems is the product of:
    - 19881 (the number of locations in a 141*141 grid)
    - 4 (the number of starting directions)

This equals 79524 possible sub-problems.

To optimize each sub-problem, the first path that the path finder checks could be the one that moves directly towards the destination,
in a zig zag pattern due to the balance constraint. (Perhaps all path finding should first move towards the target).
The algorithm should save the heat loss for this initial route as the least_heat_loss.
Every subsequent route that the path finder checks will be cancelled the moment it's heat loss exceeds the value of least_heat_loss.
If a route with a lower heat loss is found, least_heat_loss will be set to this value.

Each time the function is called, this will represent the movement of the crucible 6 possible steps:
    - Forward one, then turn left
    - Forward two, then turn left
    - Forward three, then turn left
    - Forward one, then turn right
    - Forward two, then turn right
    - Forward three, then turn right

The function will have to consider the validity of the step (whether the ending is still inside the matrix),
and the amount of heat lost during the step (checking the heat loss of every block that was passed through).
"""
