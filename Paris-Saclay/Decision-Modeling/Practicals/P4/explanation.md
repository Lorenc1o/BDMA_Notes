## Collaborative Filtering

In this practical, I have implemented the following collaborative filtering algorithms in Python:

- Eucledian and Manhattan distance
- Weighted Eucledian and Manhattan distance
- Exponential weighted Eucledian and Manhattan distance
- Pearson correlation
- Exponential weighted Pearson correlation
- Cosine similarity
- Exponential weighted cosine similarity
- Weighted Tanimoto coefficient

In addition, I have implemented functions to generate sets of ratings in which 
a) A user receives the same recommendation under all algorithms, and
b) Each algorithm recommends a different film.

### Tanimoto coefficient

This is the measure that I have added to the list of measures.

At first, I wanted to add the Jaccard coefficient, but I realized that it is not a valid measure for this task, since it does not take into account the ratings of the users, only the presence or absence of ratings.

Tanimoto accounts for this, and is defined as follows:

$$T(A,B) = \frac{\sum a_i \cdot b_i}{\sum a_i^2 + \sum b_i^2 - \sum a_i\cdot b_i},$$

where $A$ and $B$ are two vectors of ratings, and $a_i$ and $b_i$ are the ratings of the $i$-th film in $A$ and $B$, respectively.

### Generating the sets of ratings

I have followed a random approach to generate the sets of ratings. 

Basically, I generate N users, and for each of them, I generate M ratings. A rating is blank with a 40% chance, and otherwise it is a random number between 1 and 5.

Then, I generate the sets of ratings until I find one that fulfills the requirements:

- There are at least 30% of blank ratings.
- There are at most 50% of blank ratings.
- There is a user with more than 50% of blank ratings.

- A: A user receives the same recommendation under all algorithms
- B: Each algorithm recommends a different film

The results can be seen by running the script or in output.txt.

### Exercise 4

```
Generating table of critiques...
The table of critiques is:
          Person 1  Person 2  Person 3  Person 4  Person 5  Person 6  Person 7  Person 8  Person 9  Person 10
Movie 1        5.0       NaN       5.0       NaN       NaN       1.0       NaN       NaN       5.0        NaN
Movie 2        1.0       4.0       NaN       NaN       3.0       NaN       NaN       NaN       1.0        NaN
Movie 3        5.0       NaN       2.0       NaN       3.0       3.0       NaN       3.0       NaN        NaN
Movie 6        4.0       3.0       4.0       5.0       NaN       NaN       NaN       5.0       NaN        1.0
Movie 7        1.0       NaN       1.0       1.0       1.0       2.0       NaN       NaN       3.0        NaN
Movie 9        3.0       3.0       NaN       NaN       2.0       NaN       5.0       5.0       5.0        1.0
Movie 14       1.0       NaN       NaN       3.0       NaN       5.0       3.0       4.0       2.0        5.0
Movie 8        NaN       1.0       NaN       3.0       2.0       NaN       2.0       NaN       2.0        1.0
Movie 10       NaN       3.0       NaN       NaN       NaN       NaN       2.0       NaN       NaN        5.0
Movie 12       NaN       2.0       3.0       3.0       NaN       NaN       5.0       4.0       NaN        NaN
Movie 15       NaN       2.0       1.0       1.0       NaN       5.0       3.0       3.0       NaN        2.0
Movie 4        NaN       NaN       2.0       4.0       4.0       3.0       3.0       2.0       1.0        NaN
Movie 5        NaN       NaN       1.0       5.0       2.0       1.0       5.0       NaN       1.0        2.0
Movie 11       NaN       NaN       3.0       NaN       2.0       5.0       1.0       2.0       1.0        2.0
Movie 13       NaN       NaN       2.0       2.0       1.0       4.0       NaN       1.0       NaN        NaN
There are 64 NaNs in the table, that is 42.66666666666667% of the table.
The table of recommendations is:
              Best Best with exp Best with Pearson Best with cosine Best with Tanimoto
Person 1  Movie 12      Movie 12          Movie 12         Movie 12           Movie 12
```

### Exercise 5

```
Generating table of critiques...
The table of critiques is:
          Person 1  Person 2  Person 3  Person 4  Person 5  Person 6  Person 7  Person 8  Person 9  Person 10
Movie 1        2.0       3.0       4.0       2.0       4.0       NaN       NaN       NaN       NaN        4.0
Movie 3        5.0       2.0       2.0       5.0       NaN       3.0       NaN       NaN       NaN        NaN
Movie 5        3.0       NaN       2.0       NaN       NaN       NaN       1.0       NaN       4.0        NaN
Movie 6        5.0       3.0       3.0       NaN       NaN       5.0       2.0       4.0       2.0        NaN
Movie 9        4.0       2.0       NaN       NaN       2.0       1.0       NaN       1.0       NaN        3.0
Movie 10       1.0       3.0       1.0       4.0       NaN       4.0       3.0       NaN       NaN        2.0
Movie 12       3.0       4.0       4.0       NaN       NaN       NaN       2.0       3.0       NaN        NaN
Movie 14       2.0       2.0       NaN       5.0       4.0       NaN       NaN       NaN       3.0        5.0
Movie 4        NaN       2.0       3.0       4.0       NaN       NaN       NaN       1.0       2.0        NaN
Movie 8        NaN       1.0       5.0       NaN       NaN       NaN       NaN       NaN       4.0        NaN
Movie 11       NaN       4.0       NaN       4.0       5.0       1.0       2.0       2.0       NaN        NaN
Movie 13       NaN       2.0       NaN       5.0       NaN       NaN       3.0       NaN       NaN        1.0
Movie 15       NaN       2.0       NaN       1.0       NaN       NaN       5.0       3.0       3.0        NaN
Movie 2        NaN       NaN       1.0       NaN       4.0       NaN       NaN       4.0       NaN        4.0
Movie 7        NaN       NaN       1.0       2.0       NaN       1.0       4.0       2.0       5.0        NaN
There are 71 NaNs in the table, that is 47.333333333333336% of the table.
The table of recommendations is:
             Best Best with exp Best with Pearson Best with cosine Best with Tanimoto
Person 5  Movie 8       Movie 7          Movie 12          Movie 6            Movie 3
```