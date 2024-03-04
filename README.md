# 🚶‍♂️ Traveling salesman problem

Solving the travelling salesman problem using a genetic algorithm to try to get as close as possible to a correct answer in an acceptable time.
First of all, there's the genetics.py file, which handles the problem with random cities (point cloud), and then there's the barathon_genetics.py file, which tests the algorithm on the bars that took part in the last Toulouse barathon in 2023.

Here is an example of how my algorithm works for genetics.py :

![genetics_initial_population](https://github.com/Fidji32/Traveling_salesman_problem/blob/main/images/genetics_initial_population.png)
*Random cloud of points representing cities*

![genetics_results](https://github.com/Fidji32/Traveling_salesman_problem/blob/main/images/genetics_results.png)
*The first result is the best path from generation 0 and the second result is the best path found after 10000 generations.*

Here is an example of how my algorithm works for barathon_genetics.py :

![barathon_low_result](https://github.com/Fidji32/Traveling_salesman_problem/blob/main/images/barathon_low_result.png.png)
*The best way from generation 0*

![barathon_strong_result](https://github.com/Fidji32/Traveling_salesman_problem/blob/main/images/barathon_strong_result.png)
*The best way from generation 10000*
