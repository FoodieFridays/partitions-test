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
    num = Element('input-1').element.value
    length = Element('input-2').element.value

    if int(num) <= 60 and int(length) < int(num):
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
    
        # Fit various distributions to the data
        dist_names = ['alpha']
        best_dist = None        # , , , , , , , 'norm', 'expon', 'gamma', 'exponweib', 'dweibull', 'reciprocal', 'norminvgauss', 'gumbel_r'
        best_params = None
        best_sse = np.inf
    
        for dist_name in dist_names:
            dist = getattr(scipy.stats, dist_name)
            params = dist.fit(numbers)
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]
    
            # Calculate sum of squared errors (SSE)
            pdf = dist.pdf(numbers, loc=loc, scale=scale, *arg)
            sse = np.sum((relative_freq - pdf) ** 2)
    
            # Check if the current distribution provides a better fit
            if sse < best_sse:
                best_dist = dist
                best_params = params
                best_sse = sse
    
        # Plot the best-fitting distribution curve
        x = np.linspace(min(numbers), max(numbers), 100)
        y = best_dist.pdf(x, loc=best_params[-2], scale=best_params[-1], *best_params[:-2])
        plt.plot(x, y, 'r-', linewidth=2)
    
        # plt.show()
        fig
        return fig
    else:
        return "That partition is too large to run computations on OR the length value is greater than the weight. Try again with a natural number weight less than or equal to 60, with a valid length."
    
    '''
    num = Element('input-1').element.value
    length = Element('input-2').element.value

    partitions = get_integer_partitions(int(num))
    fig, ax = plt.subplots()
    
    # Redefine the partitions list to only contain partitions of the specified length (-1 default value skips this)
    if length != -1:
        partitions = [sublist for sublist in partitions if len(sublist) == length]

    multiplicities = {}
    total_numbers = 0

    for lst in partitions:
        for num in lst:
            multiplicities[num] = multiplicities.get(num, 0) + 1
            total_numbers += 1

    numbers = list(multiplicities.keys())
    counts = list(multiplicities.values())
    relative_freq = np.array(counts) / total_numbers

    plt.bar(numbers, relative_freq)
    plt.xlabel("Number")
    plt.ylabel("Relative Frequency")
    plt.title("Relative Frequency Bar Chart of Number Multiplicities")

    # Fit various distributions to the data
    dist_names = ['norm']        # Removed: , 'expon', 'gamma', 'exponweib', 'dweibull', 'reciprocal', 'norminvgauss'
    best_dist = None
    best_params = None
    best_sse = np.inf

    for dist_name in dist_names:
        dist = getattr(scipy.stats, dist_name)
        params = dist.fit(numbers)
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]

        # Calculate sum of squared errors (SSE)
        pdf = dist.pdf(numbers, loc=loc, scale=scale, *arg)
        sse = np.sum((relative_freq - pdf) ** 2)

        # Check if current distribution provides a better fit
        if sse < best_sse:
            best_dist = dist
            best_params = params
            best_sse = sse

    # Plot the best-fitting distribution curve
    x = np.linspace(min(numbers), max(numbers), 100)
    y = best_dist.pdf(x, loc=best_params[-2], scale=best_params[-1], *best_params[:-2])
    plt.plot(x, y, 'r-', linewidth=2)

    # plt.show()
    # plt.show()
    fig        # Commented out
    return fig
    '''


setup_button_listeners()
