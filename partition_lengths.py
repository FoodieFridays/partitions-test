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
    text = Element('input-1').element.value

    partitions = get_integer_partitions(int(text))
    fig, ax = plt.subplots()
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
    # plt.show()
    fig
    return fig


setup_button_listeners()
