import matplotlib.pyplot as plt

import asyncio
from pyodide import create_proxy
import numpy as np

import scipy
from scipy.stats import *


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
    print("test123")

    if int(text) <= 60:
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
    
        # Fit various distributions to the data
        dist_names = ['gumbel_r']    # 'norm', 'expon', 'gamma', 'exponweib', 'dweibull', 'reciprocal', 'norminvgauss', 
        best_dist = None
        best_params = None
        best_sse = np.inf
    
        for dist_name in dist_names:
            dist = getattr(scipy.stats, dist_name)
            params = dist.fit(lengths)
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]
    
            # Calculate sum of squared errors (SSE)
            pdf = dist.pdf(unique_lengths, loc=loc, scale=scale, *arg)
            sse = np.sum((relative_freq - pdf) ** 2)
    
            # Check if current distribution provides a better fit
            if sse < best_sse:
                best_dist = dist
                best_params = params
                best_sse = sse
    
        # Plot the best-fitting distribution curve
        x = np.linspace(min(unique_lengths), max(unique_lengths), 100)
        y = best_dist.pdf(x, loc=best_params[-2], scale=best_params[-1], *best_params[:-2])
        plt.plot(x, y, 'r-', linewidth=2)
        # plt.show()
        fig
        return fig
    else:
        return "That partition is too large to run computations on. Try again with a natural number weight less than or equal to 60."


setup_button_listeners()
