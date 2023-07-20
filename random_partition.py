from random import randint

import matplotlib.pyplot as plt

import asyncio
from pyodide import create_proxy
import numpy as np

# from partitionFunctions import random_part_of_weight


def setup_button_listeners():
    btnList = document.querySelectorAll(".button")
    for i in range(len(btnList)):
        e = document.getElementById(btnList[i].id)
        btn_event = create_proxy(process_button)
        e.addEventListener("click", btn_event)


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


async def process_button(event):
    if document.getElementById("evtMsg").innerHTML == '100':  # button plot_it
        await display_output()


def multiplicity_of_idx(i, array):
    return array.count(array[i])


def get_multiplicity_vector(array):
    array.sort(reverse=True)
    lamb = "("

    # Using our above multiplicity function to generate the multiplicity vector
    for i in range(len(array)):
        if i == 0:
            lamb += str(array[i]) + "^{" + str(multiplicity_of_idx(i, array)) + "}"
        elif array[i] != array[i - 1]:
            if i == len(array) - 1:
                lamb += ", " + str(array[i]) + "^{" + str(multiplicity_of_idx(i, array)) + "}"
            else:
                lamb += ", " + str(array[i]) + "^{" + str(multiplicity_of_idx(i, array)) + "}"

    lamb += ")"

    return lamb


async def display_output(*args, **kwargs):
    output_box = Element('output-1')

    text = Element('input-1').element.value

    remaining_weight = int(text)
    lamb = []

    # The "simple" approach to generating a random partition
    while remaining_weight > 0:
        rand = randint(1, remaining_weight)
        remaining_weight -= rand
        lamb.append(rand)

    lamb.sort(reverse=True)

    output_box.write("Array Representation: \\(" + str(lamb) + "\\), Multiplicity Vector Representation: \\(" + get_multiplicity_vector(lamb) + "\\)")

    # More code that didn't work:
    # output_box.write("\\([1^1,2^2,3^3,4^4,5^5]\\)")
    # print("Check: \( [1^1,2^2,3^3,4^4,5^5] \)")
    # output_box.write("[1^1,2^2,3^3,4^4,5^5]")
    # return lamb


setup_button_listeners()
