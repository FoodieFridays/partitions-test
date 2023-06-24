import matplotlib.pyplot as plt

import asyncio
from pyodide import create_proxy
import numpy as np


def Setup_Button_Listeners():
    btnList = document.querySelectorAll(".button")
    for i in range(len(btnList)):
        e = document.getElementById(btnList[i].id)
        btn_event = create_proxy(Process_Button)
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

'''
def len_rel_freq_chart(partitions):
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
    plt.show()
    return fig
'''

#
#
async def Process_Button(event):
    if document.getElementById("evtMsg").innerHTML == '100':  # button plot_it
        fig = await plot_it()
        pyscript.write('lineplot', fig)


async def plot_it(*args, **kwargs):
    text = Element('test-input').element.value

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


'''
    if text == "4":
        Element('test-output').element.innerText = "Correct!"
        # plt.title('4 was entered')
        # len_rel_freq_chart(get_integer_partitions(40))
    else:
        Element('test-output').element.innerText = "Incorrect."

    fig, ax = plt.subplots()
    plt.title('Year vs Population')
    year_1 = [2016, 2017, 2018, 2019, 2020, 2021]
    population_1 = [42, 43, 45, 47, 48, 50]
    year_2 = [2016, 2017, 2018, 2019, 2020, 2021]
    population_2 = [43, 43, 44, 44, 45, 45]
    plt.plot(year_1, population_1, marker='o', linestyle='--', color='g', label='Country 1')
    plt.plot(year_2, population_2, marker='d', linestyle='-', color='r', label='Country 2')
    plt.xlabel('Year')
    plt.ylabel('Population (M)')
    # plt.title('Year vs Population')
    plt.legend(loc='lower right')
    fig
    return fig
'''

Setup_Button_Listeners()