from random import randint
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def get_weight(array):
    return sum(array)


def get_num_parts(array):
    return len(array)


def multiplicity_of_idx(i, array):
    return array.count(array[i])


def get_multiplicity_vector(array):
    array.sort(reverse=True)
    lamb = "("

    # Using our above multiplicity function to generate the multiplicity vector
    for i in range(len(array)):
        if i == 0:
            lamb += str(array[i]) + "^" + str(multiplicity_of_idx(i, array))
        elif array[i] != array[i - 1]:
            if i == len(array) - 1:
                lamb += str(array[i]) + "^" + str(multiplicity_of_idx(i, array))
            else:
                lamb += ", " + str(array[i]) + "^" + str(multiplicity_of_idx(i, array))

    lamb += ")"

    return lamb


def get_young_diagram(array):
    array.sort(reverse=True)
    yd = ""

    # We use the "☐" character to represent a block in the diagram
    for num in array:
        for i in range(num):
            yd += "☐"
        yd += "\n"

    return yd


def get_conjugate(array):
    max_value = max(array)
    conjugate = []

    # This determines each part of the conjugate partition
    for i in range(1, max_value + 1):
        count = sum(1 for num in array if num >= i)
        conjugate.append(count)

    return conjugate


def get_integer_partitions(n):
    full_list = []

    # Using a recursive approach
    def sub_partition(n, k, prefix):
        if n == 0:
            full_list.append(prefix)
            return
        if k > n:
            return
        sub_partition(n, k + 1, prefix)
        sub_partition(n - k, k, prefix + [k])

    sub_partition(n, 1, [])
    return full_list


def random_part_of_weight(weight):
    remaining_weight = weight
    lamb = []

    # The "simple" approach to generating a random partition
    while remaining_weight > 0:
        rand = randint(1, remaining_weight)
        remaining_weight -= rand
        lamb.append(rand)

    lamb.sort(reverse=True)
    return lamb


def random_part_of_length(len, max):
    lamb = []

    # Generating random parts for the partition
    for i in range(1, len + 1):
        lamb.append(randint(1, max))

    lamb.sort(reverse=True)
    return lamb


def len_rel_freq_chart(partitions):
    # Array to store the various lengths of the partitions
    lengths = [len(lamb) for lamb in partitions]
    unique_lengths, counts = np.unique(lengths, return_counts=True)
    # Adjusting for relative frequency
    relative_freq = counts / len(partitions)

    # matplotlib chart setup
    plt.bar(unique_lengths, relative_freq)
    plt.xlabel("Length of Lambda")
    plt.ylabel("Relative Frequency")
    plt.title("Relative Frequency Chart of Partition Lengths")
    plt.show()


# Computes the relative multiplicity distribution; can optionally specify partition length:
def mult_rel_freq_chart(partitions, length=-1):
    # Redefine the partitions list to only contain partitions of the specified length (-1 default value skips this)
    if length != -1:
        partitions = [sublist for sublist in partitions if len(sublist) == length]

    # Using a dictionary for the multiplicities (keys -> number, values -> multiplicity)
    multiplicities = {}
    total_numbers = 0

    # Count the multiplicities of numbers in the lists
    for lst in partitions:
        for num in lst:
            multiplicities[num] = multiplicities.get(num, 0) + 1
            total_numbers += 1

    # Convert the dictionary values to lists
    numbers = list(multiplicities.keys())
    counts = list(multiplicities.values())
    # Adjusting for relative frequency
    relative_freq = np.array(counts) / total_numbers

    # matplotlib chart setup
    plt.bar(numbers, relative_freq)
    plt.xlabel("Number")
    plt.ylabel("Relative Frequency")
    plt.title("Relative Frequency Bar Chart of Number Multiplicities")
    plt.show()


def maya_diagram(partition, charge):
    partition.sort(reverse=True)

    # Various sets defined in Nathan's paper
    s_plus = []
    s_minus = []
    maya_output = []

    # Numbers to go in s_plus
    for i in range(len(partition)):
        if partition[i] > i:
            s_plus.append(partition[i] - i)
        else:
            break

    # Numbers to go into s_minus
    for i in range(1, len(partition)):
        if sum(num >= i for num in partition) - i >= 1:
            s_minus.append((sum(num >= i for num in partition) - i) * -1)
        else:
            break

    # Numbers to go into s_plus
    for num in s_plus:
        maya_output.append(num)

    # Adding 0 into the final output
    maya_output.append(0)

    # Appending to the final output, plus a few more at the end
    for i in range(-1, min(s_minus) - 3, -1):
        if i not in s_minus:
            maya_output.append(i)

    # Adjusting for the charge, if needed
    if charge != 0:
        for i in range(len(maya_output)):
            maya_output[i] += charge

    # Creating the visual diagram
    visual = ""
    for i in range(max(maya_output), min(maya_output) - 3, -1):
        if i in s_plus or i in s_minus:
            visual += "● "
        else:
            visual += "○ "

    # Appending the visual diagram to the final output
    maya_output.append("... Visual: " + visual + "...")

    return maya_output


def partition_from_maya(maya_set, charge):
    # Various sets defined in Nathan's paper
    s_plus = []
    s_minus = []

    # A "helper" set
    s_minus_adjust = []

    # Final output
    partition = []

    # Adjust for a charge, if needed
    if charge != 0:
        for i in range(len(maya_set)):
            maya_set[i] -= charge

    # Numbers to go into s_plus
    for i in range(len(maya_set)):
        if maya_set[i] != 0:
            s_plus.append(maya_set[i])
        else:
            break

    # Adjusting numbers from s_plus to go into the partition
    for i in range(len(s_plus)):
        partition.append(s_plus[i] + i)

    # Numbers to go into s_minus
    for i in range(-1, min(maya_set) - 1, -1):
        if i not in maya_set:
            s_minus.append(i)

    # Numbers to go into the s_minus adjusted set
    for num in s_minus:
        s_minus_adjust.append(-1 * num)

    for i in range(len(s_minus_adjust)):
        s_minus_adjust[i] -= i

    # Based on s_minus_adjusted, we compute the additional numbers that must be added to the partition
    for i in range(1, max(s_minus_adjust) + 1):
        count = sum(num >= i for num in s_minus_adjust)
        partition.append(count)

    return partition


# Some examples to run, if desired:

# print(random_part_of_length(10, 10))
# print(random_part_of_weight(10))
# print(get_integer_partitions(10))
# print(get_young_diagram([5, 4, 4, 2]))
# len_rel_freq_chart(get_integer_partitions(70))
# mult_rel_freq_chart(get_integer_partitions(40))
# print(partition_from_maya([4, 3, 1, 0, -2, -3, -5, -7, -8], 0))
# print(maya_diagram([4, 4, 3, 3, 2, 2, 1], 2))
# print(partition_from_maya([6, 5, 3, 2, 0, -1, -3, -5, -6], 2))
