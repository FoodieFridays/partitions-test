from pyodide import create_proxy


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
    output_box_1 = Element('output-1')
    output_box_2 = Element('output-2')

    text = Element('input-1').element.value
    charge = int(Element('input-2').element.value)

    str_arr = text.split(",")
    partition = []

    for num in str_arr:
        partition.append(int(num))

    partition.sort(reverse=True)

    # Various sets defined in Nathan's paper
    s_plus = []
    s_minus = []
    maya_output = []

    # Numbers to go in s_plus
    for i in range(len(partition)):
        if partition[i] > i:
            s_plus.append(partition[i] - i)
        else:
            break

    # Numbers to go into s_minus
    for i in range(1, len(partition)):
        if sum(num >= i for num in partition) - i >= 1:
            s_minus.append((sum(num >= i for num in partition) - i) * -1)
        else:
            break

    # Numbers to go into s_plus
    for num in s_plus:
        maya_output.append(num)

    # Adding 0 into the final output
    maya_output.append(0)

    # Appending to the final output, plus a few more at the end
    for i in range(-1, min(s_minus) - 3, -1):
        if i not in s_minus:
            maya_output.append(i)

    # Adjusting for the charge, if needed
    if charge != 0:
        for i in range(len(maya_output)):
            maya_output[i] += charge

    # Creating the visual diagram
    visual = ""
    for i in range(max(maya_output), min(maya_output) - 3, -1):
        if i in s_plus or i in s_minus:
            visual += "● "
        else:
            visual += "○ "

    # Appending the visual diagram to the final output
    maya_output.append(visual + "...")

    output_box_1.write("Numerical Diagram: \\(" + str(maya_output[:len(maya_output) - 1]) + "\\)")
    output_box_2.write("Visual Diagram: " + maya_output[-1])


setup_button_listeners()
