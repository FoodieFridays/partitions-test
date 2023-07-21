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
    if document.getElementById("evtMsg").innerHTML == '100':    # When button is clicked
        await display_output()


async def display_output(*args, **kwargs):
    output_box = Element('output-1')

    text = Element('input-1').element.value

    str_arr = text.split(",")
    int_arr = []

    for num in str_arr:
        int_arr.append(int(num))

    max_value = max(int_arr)
    conjugate = []

    # This determines each part of the conjugate partition
    for i in range(1, max_value + 1):
        count = sum(1 for num in int_arr if num >= i)
        conjugate.append(count)

    output_box.write("The conjugate partition of \\(" + str(int_arr) + "\\) is \\(" + str(conjugate) + "\\)")

setup_button_listeners()
