import math
import itertools


# This function returns True if x divides y and False otherwise.
def divides(x, y):
    return y % x == 0


# This function returns True if the integer x is prime, and False otherwise.
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


# This function takes as input a positive integer and returns a two-dimensional array.
# The firs row is
# a list of k's prime divisors, ordered increasingly, and the second row is a list of
# the exponents of
# prime divisor.
def prime_divisors(k):
    divisors = []
    exponents = []
    divisor = 2
    while divisor ** 2 <= k:
        exponent = 0
        while divides(divisor, k):
            exponent += 1
            k //= divisor

        if exponent > 0:
            divisors.append(divisor)
            exponents.append(exponent)

        divisor += 1

    if k > 1:
        divisors.append(k)
        exponents.append(1)

    return [divisors, exponents]


# The following function returns a broad list of candidate minimally k-irreducible
# sums. For any minimally k-irreducible sum a_1d_1 + ,,, + a_nd_n, the corresponding
# vector [a_1, ..., a_n] is guaranteed to belong to the list candidate_vectors(k).
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
# .., x_n], the following function outputs the total of the
# sum x_1d_1 + ... + x_nd_n.
def corresponding_sum_total(x, k):
    D = proper_divisors(k)
    n = len(D)
    sum = 0
    for i in range(0, n):
        sum += x[i] * D[i]
    return sum


# Given a positive integer k with proper divisors d_1, ..., d_n and a positive integer
# c>=2, the following function outputs the set V of all vectors [x_1, ..., x_n] satisfying
# x_1d_1 + ... + x_nd_n = ck.
def candidate_vectors_with_total_ck(c, k):
    U = candidate_vectors(k)
    V = []
    for x in U:
        if corresponding_sum_total(x, k) == c * k:
            V.append(x)
    return V


print(candidate_vectors_with_total_ck(2, 42))


# Given a positive integer k with proper divisors d_1, ..., d_n, the following function
# takes as input a vector x = [x_1, ..., x_n], makes a list of all vectors y = [y_1,
# ..., y_n] satisfying
# 0<=y_i<=x_i for all 1<=i<=n and y_1 + ... + y_n >= 2, and outputs True if one such y
# has a corresponding total dividing k, and outputs False otherwise.
def admits_subsum_with_total_dividing_k(x, k):
    D = proper_divisors(k)
    n = len(D)
    I = []  # The entries of the list I will be the closed intervals [1, x_i] for 0<=i<=n.
    for i in range(0, n):
        I.append([*range(0, x[i] + 1)])
    X = list(itertools.product(
        *I))  # A list representing the cartesian product of every interval in I.
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


# The following function takes as input positive integers c and k and outputs a list of
# all minimally k-irreducible sums with total ck.
def all_minimally_k_irreducible_sums_with_total_ck(c, k):
    V = candidate_vectors_with_total_ck(c, k)
    L = []  # List of all vectors corresponding to minimally k-irreducible sums with
    # total ck.
    for x in V:
        if not admits_subsum_with_total_dividing_k(x, k):
            L.append(x)
    return L


# The following function takes as input a positive integer k and a vector x = [x_1,
# ..., x_n] and returns the string 'x_1d_1 + ... + x_nd_n', the sum corresponding to x.
def vector_as_sum(k, x):
    D = proper_divisors(k)
    n = len(D)
    s = ""
    # Append 'x_id_i + ' to s for all 0 <= i <= n-1.
    for i in range(0, n):
        if x[i] != 0:
            s = s + str(x[i]) + "*" + str(D[i]) + " + "
    # Remove the superfluous ' + ' at the end of s
    s = s[0:len(s) - 3]
    return s


# Prompt user to input a value of c and k.
integers = input("input positive integers c > 1 and k > 1 separated by a space: ").split()
# Display the list of all minimally k-irreducible sums with total ck.
list = all_minimally_k_irreducible_sums_with_total_ck(int(integers[0]), int(integers[1]))
if len(list) == 0:
    print("There are no k-irreducible sums with total ck for the chosen values.")
else:
    print("List of all minimally k-irreducible sums with total ck:")
    for x in list:
        print(vector_as_sum(int(integers[1]), x))
input()