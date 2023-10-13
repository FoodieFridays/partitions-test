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


def get_integral_pyramid(partition):
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

    user_arr = text.split(",")
    arr = get_integral_pyramid(user_arr)

    fig, ax = plt.subplots()
    current_x = 0

    for block_height in arr:
        rect = patches.Rectangle((current_x, 0), 1, block_height, linewidth=2, edgecolor='black', facecolor='blue')
        ax.add_patch(rect)
        current_x += 1

    ax.set_xlim(0, current_x)
    ax.set_ylim(0, max(arr))
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    plt.show()
    fig
    return fig


setup_button_listeners()