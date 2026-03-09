[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2r7IDe_N)

# AI Assignment 02 - R-R


## Reporting Win Rate

| Player A   | A wins | Player B   | B wins |
|------------|--------|------------|--------|
| Random     | 0.01   | Heuristic  | 0.97   |
| Heuristic  | 0.52   | Minimax    | 0.43   |
| Random     | 0.02   | Minimax    | 0.97   |



## Is R-R Fair?


By alternating who starts each game, we ensure that any first-player advantage would be easy to spot. Random vs Heuristic and Random vs Minimax both show the stronger player dominating with 0.97 regardless of which player goes first. The matchup that stands out the most is Heuristic vs Minimax, and despite Minimax being the stronger player, Heuristic wins with 0.52 against 0.43. Since none of the matchups show a pettern where going first means consisitently winning, therefore we can say that there isn't any first-move advantage in R-R. So R-R appears to be fair.  

## Use of LLM 
- I used Claude to help me break down the assignment spec, and understand what needed to be implemented. 
- I also asked Claude to explain the time complexity, and why it took so long to run all 300 games. 
- Here are some of my prompts: 
--> How is the remove rule affecting the runtime? Does it effect it at all? 
--> Copying the board for every move on a 16x16 board probably makes thr simulation run much slower, can we get rid of it entirely? 


- I found Claude to be very helpful, especially for explaining why the program took so long to run. 
- Claude also made the rules and instructions easier to grasp, by generating a rule book. 
- It helped me break down the key concepts/steps and implement the different parts effectively. 