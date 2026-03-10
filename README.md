[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2r7IDe_N)

# AI Assignment 02 - R-R


## Reporting Win Rate

| Player A   | A wins | Player B   | B wins |
|------------|--------|------------|--------|
| Random     | 0.05   | Heuristic  | 0.93   |
| Heuristic  | 0.53   | Minimax    | 0.45   |
| Random     | 0.01   | Minimax    | 0.99   |

## Fairness Comparison (Playes Against Themselves)

| Player A   | A wins | Player B   | B wins |
|------------|--------|------------|--------|
| Random     | 0.46   | Random     | 0.32   |
| Heuristic  | 0.52   | Heuristic  | 0.46   |
| Minimax    | 0.53   | Minimax    | 0.47   |


## Is R-R Fair?


By alternating who starts each game, we ensure that any first-player advantage would be easy to spot. Random vs Heuristic and Random vs Minimax both show the stronger player dominating with 0.93-0.99 regardless of which player goes first. The matchup that stands out the most is Heuristic vs Minimax, and despite Minimax being the stronger player, Heuristic wins with 0.53 against 0.45. 

Comparing Random vs itself shows a little unbalance with 0.46 against 0.32. Heuristic vs itself doesn't show any first move advantage with 0.52 against 0.46. Finally, Minimax vs itself is the strongest indicator of fairness, with 0.53 against 0.47.     

Since none of the matchups show a pettern where going first means consisitently winning, we can say that there isn't any first-move advantage in R-R. So R-R appears to be fair.  


## Use of LLM 
- I used Claude to help me break down the assignment spec, and understand what needed to be implemented. 
- I also asked Claude to explain the time complexity, and why it took so long to run all 300 games. 
- Here are some of my prompts: 
- How is the remove rule affecting the runtime? Does it affect it at all? 
- Copying the board for every move on a 16x16 board probably makes thr simulation run much slower, can we get rid of it entirely? 


- I found Claude to be very helpful, especially for explaining why the program took so long to run. 
- Claude also made the rules and instructions easier to grasp, by generating a rule book. 
- It helped me break down the key concepts/steps and implement the different parts effectively. 