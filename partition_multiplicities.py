import matplotlib.pyplot as plt

import asyncio
from pyodide import create_proxy
import numpy as np


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
        fig = await display_output()
        pyscript.write('user-IO', fig)


async def display_output(*args, **kwargs):
    num = Element('input-1').element.value
    length = Element('input-2').element.value

    partitions = get_integer_partitions(int(num))
    fig, ax = plt.subplots()
    # Redefine the partitions list to only contain partitions of the specified length (-1 default value skips this)
    if int(length) != -1:
        partitions = [sublist for sublist in partitions if len(sublist) == int(length)]

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
    plt.title("Relative Frequency Bar Chart of Number Multiplicities (of length " + length + ")")
    # plt.show()

    # fig
    return fig


setup_button_listeners()
