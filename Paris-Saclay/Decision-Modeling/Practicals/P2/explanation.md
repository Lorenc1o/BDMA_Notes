## Linear programming and preferences

This program provides the solutions to the practical 2 session.

1. **p2_ex1.py**: I solve the toy manufacturing problem.
2. **p2_ex2.py**: I solve the visit to Paris problem. Let's focus on this program, which is more complex.

### Base problem

I have implemented the model in the file `p2_ex2.py`. The model is as follows:

- Decision variables:
    - `x`: `x[i]` is a binary variable, indicating if place `i` is visited or not.

- Objective function:
    - `maximize sum(x[i] for i in range(n))` (maximize the number of visited places)

- Constraints:
    - `sum(time[i] * x[i] for i in range(n)) <= 12` (the total time spent in the visited places must be less than 12 hours)
    - `sum(cost[i] * x[i] for i in range(n)) <= 65` (the total cost of the visited places must be less than 65 euros)

### Preferences

I have implemented a function to add the different additional constraints as needed. The function is called `solve_with_preferences`. This way, the code is more readable.

The preferences are implemented as follows:
- Preference 1: If two places are within 1km of each other, then they should be visited together.
    - Modelled as a constraint: `x[i] == x[j]` if `distance[i][j] <= 1`
- Preference 2: Visit TE and CA.
    - Modelled as a constraint: `x[i] == 1` and `x[j] == 1` where `i` is the index of TE and `j` is the index of CA.
- Preference 3: If CN is visited, then SC is not visited.
    - Modelled as a constraint: `x[i] + x[j] <= 1` where `i` is the index of CN and `j` is the index of SC.
- Preference 4: TM is visited.
    - Modelled as a constraint: `x[i] == 1` where `i` is the index of TM.
- Preference 5: If ML is visited, then CP is visited.
    - Modelled as a constraint: `x[i] - x[j] <= 0` where `i` is the index of ML and `j` is the index of CP.

The different solutions are compared through the function `compare_solutions`. The function prints a comparison of the two solutions given as input, checking which places changes from the first solution to the second one. 

The full output of the program can be read in the file `p2_ex2_output.txt`. The important part to this point is:

```
----------------------------------------------
Summary:
Preference           	Sites to visit                            	Number of sites	Same as base problem?	
Base problem         	['AC', 'AT', 'BS', 'CA', 'CN', 'PC', 'SC']	7              	True                 
Pref 1               	['AC', 'AT', 'CA', 'JT', 'MO', 'PC', 'TM']	7              	False                
Pref 2               	['AC', 'AT', 'CA', 'PC', 'SC', 'TE']      	6              	False                
Pref 3               	['AC', 'AT', 'BS', 'CA', 'MO', 'PC', 'SC']	7              	False                
Pref 4               	['AC', 'AT', 'BS', 'CN', 'PC', 'SC', 'TM']	7              	False                
Pref 5               	['AC', 'AT', 'BS', 'CA', 'CN', 'PC', 'SC']	7              	True                 
Pref 1 and 2         	['AC', 'AT', 'CA', 'TE', 'TM']            	5              	False                
Pref 1 and 3         	['AC', 'AT', 'CA', 'JT', 'MO', 'PC', 'TM']	7              	False                
Pref 1 and 4         	['AC', 'AT', 'CA', 'JT', 'MO', 'PC', 'TM']	7              	False                
Pref 2 and 5         	['AC', 'AT', 'CA', 'PC', 'SC', 'TE']      	6              	False                
Pref 3 and 4         	['AC', 'AT', 'BS', 'CA', 'PC', 'SC', 'TM']	7              	False                
Pref 4 and 5         	['AC', 'AT', 'BS', 'CN', 'PC', 'SC', 'TM']	7              	False                
Pref 1, 2 and 4      	['AC', 'AT', 'CA', 'TE', 'TM']            	5              	False                
Pref 2, 3 and 5      	['AC', 'AT', 'CA', 'JT', 'PC', 'TE']      	6              	False                
Pref 2, 3, 4 and 5   	['AC', 'AT', 'CA', 'PC', 'TE', 'TM']      	6              	False                
Pref 1, 2, 4 and 5   	['AC', 'AT', 'CA', 'TE', 'TM']            	5              	False                
Pref 1, 2, 3, 4 and 5	['AC', 'AT', 'CA', 'TE', 'TM']            	5              	False                
----------------------------------------------
```

As we can see, the only preference that does not change the solution is preference 5 alone. All the other preferences change the visit, but some of them do not change the amount of places visited.

### Rankings

I have implemented the three rankings explained in the practical session, allowing for ties.

Then, since there are no Python libraries implementing the kendall and spearman coefficients for total preorders, I have implemented these functions myself. The code is in the file `p2_ex2.py`.

The output is as follows (the full output is in the file `ex2_output.txt`):

```
----------------------------------------------
Computing the preference relation DUR...
[['TE'], ['ML'], ['CP'], ['MO', 'CA', 'CN', 'BS', 'TM'], ['JT', 'SC', 'AC'], ['AT'], ['PC']]
----------------------------------------------
Computing the preference relation APP...
[['AT', 'JT', 'PC'], ['MO', 'TM'], ['CP', 'SC'], ['TE', 'CN', 'AC'], ['ML', 'CA', 'BS']]
----------------------------------------------
Computing the preference relation PRI...
[['JT', 'PC', 'AC'], ['CN'], ['BS', 'SC'], ['AT'], ['CA', 'CP'], ['MO'], ['ML'], ['TE', 'TM']]
----------------------------------------------
The Kendall coefficient between DUR and APP is:
-0.5152106565919433
----------------------------------------------
The Kendall coefficient between DUR and PRI is:
-0.7016464154456233
----------------------------------------------
The Kendall coefficient between APP and PRI is:
0.11518245674418136
----------------------------------------------
The Spearman coefficient between DUR and APP is:
-0.6232538633263821
----------------------------------------------
The Spearman coefficient between DUR and PRI is:
-0.7405359377080045
----------------------------------------------
The Spearman coefficient between APP and PRI is:
0.24753688574416854
----------------------------------------------
```

Therefore, we can draw the following conclusions:
- High disagreement between DUR and the others:
	In both metrics, DUR is quite strongly negatively related to the other rankings.
	This is an indication that prices and appreciations are not taking the duration too much into account, or even that shorter visits are preferred and more expensive.
- Slight agreement between APP and PRI:
	In both metrics, these two rankings present a slight possitive correlation.
	This indicates that the visitors take the price into account for their appreciations.
- Agreement between the two metrics:
	The two metrics present very similar results, increasing our confidence in the conclusions.