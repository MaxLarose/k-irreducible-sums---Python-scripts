import itertools
import math


# This function returns True if x divides y and False otherwise.
def divides(x, y):
    return y % x == 0


# This function returns True if the positive integer x is prime, and False otherwise.
def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if divides(i, x):
            return False
    return True


# This function takes as input a positive integer k and returns a list of its proper
# divisors, ordered increasingly.
def proper_divisors(k):
    # Define D to be an empty list. It will represent the list of all proper divisors
    # of k.
    D = []
    for i in range(1, k):
        if divides(i, k):
            D.append(i)
    return D


# This function takes as input a positive integer x and returns the smallest prime
# divisor of x.
def smallest_prime_divisor(x):
    for i in range(2, x + 1):
        if divides(i, x) and is_prime(i):
            return i


# The following function returns a broad list of candidate minimally k-irreducible
# sums. It is the cartesian product of all the closed intervals [0, p_d - 1] (for
# proper divisors d of k) where p_d is the smallest prime divisor of k/d. For any
# minimally k-irreducible sum a_1d_1 + ,,, + a_nd_n, the corresponding vector [a_1,
# ..., a_n] is guaranteed to belong to the list candidate_vectors(k).
def candidate_vectors(k):
    D = proper_divisors(k)
    n = len(D)  # D is the list [d_1, d_2, ..., d_n] of proper divisors of k.
    I = []
    for i in range(0, n):
        # Define I[i+1] to be the interval of integers j with 0 <= j <= p_i - 1 where
        # p_i is the smallest prime divisor of k/d_i
        I.append([*range(0, smallest_prime_divisor(k // D[i]))])
    return list(itertools.product(*I))


# Given a positive integer k with proper divisors d_1, ..., d_n and a vector x = [x_1,
# .., x_n], the following function outputs the total of the sum x_1d_1 + ... + x_nd_n.
def corresponding_sum_total(x, k):
    D = proper_divisors(k)
    n = len(D)
    sum = 0
    for i in range(0, n):
        sum += x[i] * D[i]
    return sum


# Given a positive integer k with proper divisors d_1, ..., d_n, the following function
# takes as input a vector x = [ x_1, ..., x_n], makes a list of all vectors y = [y_1,
# ..., y_n] satisfying 0<=y_i<=x_i for all 1<=i<=n and y_1 + ... + y_n >= 2,
# and outputs True if one such y has a corresponding total dividing k, and outputs
# False otherwise.
def admits_subsum_with_total_dividing_k(x, k):
    D = proper_divisors(k)
    n = len(D)
    I = []  # The entries of the list I will be the closed intervals [1, x_i] for 0<=i<=n.
    for i in range(0, n):
        I.append([*range(0, x[i] + 1)])
    X = list(itertools.product(*I))  # A list representing the cartesian product of
    # every interval in I.

    # Define Y to be the sublist of X obtained by removing the vector [0,...,0] as well
    # as any vector of the form [0, ..., 0, 1, 0, ..., 0] (i.e. any vector with a
    # 1-norm less than 2) as we are only interested in non-trivial subsums.
    Y = []
    for x in X:
        if sum(x) > 1:
            Y.append(x)
    # We check the total of the sums corresponding to each vector in X. If one of the
    # totals is a divisor of k, then the function returns True. Otherwise it returns
    # False.
    for y in Y:
        if divides(corresponding_sum_total(y, k), k):
            return True
    return False


# The following function takes as input a positive integer k and outputs a list of all
# vectors corresponding to weak minimally k-irreducible sums.
def all_weak_minimally_k_irreducible_sums(k):
    X = candidate_vectors(k)
    list = []  # Define list to be an empty list. Append to it every vector in X whose
    # corresponding sum is weak
    # minimally k-irreducible.
    for x in X:
        if not admits_subsum_with_total_dividing_k(x, k):
            list.append(x)
    return list


# This function takes a positive integer n as input and outputs the number of prime
# divisors of n.
def number_of_prime_divisors(n):
    count = 0
    for i in range(2, int(n + 1)):
        if divides(i, n) and is_prime(i):
            count += 1
    return count


# This function takes as input a positive integer n and outputs True if n is a product
# of two primes and False otherwise.
def is_product_of_two_primes(n):
    if number_of_prime_divisors(n) == 2 and is_prime(int(n / smallest_prime_divisor(n))):
        return True
    else:
        return False


# The following function takes as input a positive integer k and outputs F(k),
# the maximum total achievable by a weak k-irreducible sum.
def max_weak_k_irreducible_sum_total(k):
    # In the case where k is a prime power or a product of two primes, we apply a known
    # formula to obtain the maximum total.
    if number_of_prime_divisors(k) == 1:
        return k - 1
    if is_product_of_two_primes(k):
        p = smallest_prime_divisor(k)
        q = int(k / p)
        return (p - 1) * q + (q - 1) * p
    # In the remaining cases, we proceed by brute force:
    X = all_weak_minimally_k_irreducible_sums(k)
    totals = []  # Define totals to be the empty list. For every vector x in X,
    # append the total of the sum corresponding to x.
    for x in X:
        totals.append(corresponding_sum_total(x, k))
    return max(totals)


# Prompt the user to input an integer k > 1 and print the value of F(k)
print("F(k) = ", max_weak_k_irreducible_sum_total(int(input("Input an integer k > 1: "))))
input()