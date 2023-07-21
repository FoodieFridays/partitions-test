from random import randint

import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
                lamb += ", " + str(array[i]) + "^" + str(multiplicity_of_idx(i, array))
            else:
                lamb += ", " + str(array[i]) + "^" + str(multiplicity_of_idx(i, array))

    lamb += ")"

    return lamb


async def process_button(event):
    if document.getElementById("evtMsg").innerHTML == '100':  # button plot_it
        fig = await display_output()
        pyscript.write('user-IO', fig)


async def display_output(*args, **kwargs):
    # plt.rcParams['text.usetex'] = True        # Added for LaTeX

    text = Element('input-1').element.value

    text_arr = text.split(",")
    int_arr = []

    for num in text_arr:
        int_arr.append(int(num))

    int_arr.sort(reverse=True)

    rows = len(int_arr)
    max_blocks = max(map(int, int_arr))

    fig, ax = plt.subplots()

    for row, num_blocks in enumerate(int_arr, 1):
        num_blocks = int(num_blocks)
        for i in range(max_blocks):
            if i < num_blocks:
                rect = patches.Rectangle((i, rows - row), 1, 1, linewidth=1, edgecolor='black', facecolor='blue')
                ax.add_patch(rect)

    ax.set_xlim(0, max_blocks)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.title("Young Diagram for lambda = " + get_multiplicity_vector(int_arr))
    # plt.title(r'\textbf{time (s)}')
    # plt.show()
    fig
    return fig


setup_button_listeners()
