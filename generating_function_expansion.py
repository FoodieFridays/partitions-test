from random import randint

import matplotlib.pyplot as plt

import asyncio
from pyodide import create_proxy

import numpy
from numpy.polynomial import Polynomial


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

    n = int(text)
    
    polynomials = []
        
    for i in range(n):
        polynomials.append([0] * (n + 1))
        polynomials[i][0] = 1
    
        for j in range(1, n + 1):
            if (i + 1) * j <= n:
                polynomials[i][(i + 1) * j] = 1
    
    polynomials_numpy = []
    
    for i in range(len(polynomials)):
        polynomials_numpy.append(Polynomial(polynomials[i]))
    
    result = polynomials_numpy[0]
    
    for i in range(1, len(polynomials_numpy)):
        result = numpy.polymul(result, polynomials_numpy[i])[0]
    
    str_result = str(result)
    # p_n = float(str_result[str_result.find("x**" + str(n - 1)) + len("x**" + str(n)) + 3:str_result.find("x**" + str(n))])        ### COMMENTED OUT
    
    # print("\nPolynomial Expansion:\n")
    # print(str_result[:str_result.find("x**" + str(n)) + len("x**" + str(n))] + " + ... [inaccurate higher degree terms]")
    # print("Thus, the number of integer partitions of weight n=" + str(n) + " is " + str(p_n))

    # output_box.write(str_result[:str_result.find("x**" + str(n)) + len("x**" + str(n))] + " + ... [inaccurate higher degree terms]")
    # output_box.write("Hello")
    output_box.write(str_result + "\n\n(The coefficients are accurate up to the x**" + str(n) + " term.")

setup_button_listeners()
