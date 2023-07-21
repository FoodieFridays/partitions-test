from random import randint

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
        await display_output()


async def display_output(*args, **kwargs):
    output_box = Element('output-1')

    text = Element('input-1').element.value
    charge = int(Element('input-2').element.value)

    str_arr = text.split(",")
    maya_set = []

    for num in str_arr:
        maya_set.append(int(num))

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

    output_box.write("\\(" + str(partition) + "\\)")


setup_button_listeners()
