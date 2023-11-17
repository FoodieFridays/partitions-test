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


def get_int_pyr(partition):
    partition.sort()

    int_pyr_len = len(partition) + max(partition) - 1
    outputs = []
    
    for i in range(0, int_pyr_len):
        outputs.append(1)
    
    for i in range(1, int_pyr_len):
        j = i
        n = 2
        if i >= len(partition):
            n += i - len(partition) + 1
            j = len(partition) - 1
    
        while j - 1 > 0 and partition[j - 1] >= n:
            outputs[i] += 1
            j -= 1
            n += 1
    
            if j - 1 < 0:
                break
    
    return outputs


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

    int_arr = get_int_pyr(int_arr)
    
    fig, ax = plt.subplots()
    current_x = 0

    for block_height in int_arr:
        rect = patches.Rectangle((current_x, 0), 1, block_height, linewidth=2, edgecolor='black', facecolor='blue')
        ax.add_patch(rect)
        current_x += 1

    ax.set_xlim(0, current_x)
    ax.set_ylim(0, max(int_arr))
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    plt.title("Integral Pyramid for lambda = " + str(int_arr))

    plt.show()
    fig
    return fig


setup_button_listeners()
