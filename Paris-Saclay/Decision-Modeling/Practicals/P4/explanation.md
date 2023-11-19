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