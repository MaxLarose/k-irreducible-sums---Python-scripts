import math


# This function takes as input positive integers m and h from an acceptable parameter
# set alpha, m, h and outputs a list of all values of r for which the integers m,
# alpha*m, h, r, s (with s = h) are feasible.
def possible_values_of_r(m, h):
    list = []
    binomial_coefficient = math.comb(m - 1, h - 1)
    for r in range(1, h + 1):
        if m * r % h == 0 and binomial_coefficient % r == 0:
            list.append(r)
    return list


# Create an array acceptable_integers whose 0 entry is the value of m inputted by the
# user and whose 1 entry is the value of h inputted by the user.
acceptable_integers = input("Enter m and h seperated by a space: ").split()
print("The possible values of r are:")
# Print each element of the list acceptable_integers.
for i in possible_values_of_r(int(acceptable_integers[0]), int(acceptable_integers[1])):
    print(i)
input()
