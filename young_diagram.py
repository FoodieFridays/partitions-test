from random import randint

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


async def Process_Button(event):
    if document.getElementById("evtMsg").innerHTML == '100':  # button plot_it
        fig = await plot_it()
        # pyscript.write('lineplot', fig)


async def plot_it(*args, **kwargs):
    output_box = Element('test-output')

    text = Element('test-input').element.value

    str_arr = np.array(text.split(","))
    int_arr = []

    for num in str_arr:
        int_arr.append(int(num))

    int_arr.sort(reverse=True)
    yd = ""

    # We use the "☐" character to represent a block in the diagram
    for num in int_arr:
        for i in range(num):
            yd += "☐"
        yd += "\n"

    output_box.write(yd)


Setup_Button_Listeners()
