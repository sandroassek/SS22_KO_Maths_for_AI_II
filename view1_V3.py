import copy

from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox


def dft(dx, L, n, x, f):
    A = np.zeros(n)
    B = np.zeros(n)

    A0 = np.sum(f * np.ones_like(x)) * dx
    for k in range(n):
        #A[k] = np.sum(f * 2 * np.cos(2 * np.pi * (k + 1) * x)) * dx
        A[k] = 2 * np.sum(f * np.cos(2 * np.pi * (k + 1) * x / L)) * dx
        B[k] = 2 * np.sum(f * np.sin(2 * np.pi * (k + 1) * x / L)) * dx
    return A0, A, B


def func_from_factors(x, L, A0, A, B, n):
    fFS = A0
    for k in range(n):
        fFS = fFS + A[k] * np.cos((k + 1) * 2 * np.pi * x / L) + B[k] * np.sin((k + 1) * 2 * np.pi * x / L)
    return fFS


def vis_1(dx, L, n=1, function="x"):
    x = L * np.arange(-dx, 1-dx, dx)

    f1 = eval(function)

    A0, A, B = dft(dx, L, n, x, f1)

    f2 = func_from_factors(x, L, A0, A, B, n)

    return x, f1, f2


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)

x, f1, f2 = vis_1(0.001, 1, 10, "np.sin(2*np.pi*x)")

l1, = ax.plot(x, f1)
l2, = ax.plot(x, f2)


def update(val):
    test[0] = int(red.val // 1)

    l1.set_ydata(eval("np.sin(2*np.pi*x)"))
    x, f1, f2 = vis_1(0.001, 1, int(test[0]), test[1])

    l1.set_ydata(f1)
    l2.set_ydata(f2)


def submit(expression):
    test[1] = expression
    x, f1, f2 = vis_1(0.001, 1, int(test[0]), test[1])

    l1.set_ydata(f1)
    l2.set_ydata(f2)
    ax.relim()
    ax.autoscale_view()
    plt.draw()

test = [1, "x"]

r = 1
axred = fig.add_axes([0.25, 0.2, 0.65, 0.03])
red = Slider(axred, 'n', 0.0, 50.0, 1, valstep=1)
red.on_changed(update)

e = "x"
axbox = fig.add_axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(axbox, "Evaluate")
text_box.on_submit(submit)
text_box.set_val("x")  # Trigger `submit` with the initial string.

plt.show()
