import numpy as np
from scipy import interpolate
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt
import sys


class FunctionDrawer:
    def __init__(self):
        self.x = []
        self.y = []
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        plt.xlim(0, 1)
        plt.ylim(-5, 5)
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.title('Function Drawing')

        plt.grid()

        plt.connect('button_press_event', self._on_mouse_click)
        self.fig.canvas.mpl_connect('close_event', self._on_window_close)

        plt.connect('key_press_event', self._on_key_click)

        plt.show()

    def _on_key_click(self, event):
        sys.stdout.flush()

        if event.key == 'escape':
            FunctionApproximator(self._get_fct_values())

    def _on_mouse_click(self, event):
        if event.button is MouseButton.RIGHT:
            clicked_x, clicked_y = event.xdata, event.ydata
            if clicked_x is None and clicked_y is None: return
            if len(self.x) == 0 and len(self.y) == 0:
                self.x += [clicked_x]
                self.y += [clicked_y]
                plt.plot(clicked_x, clicked_y, 'bo')
            else:
                # check if new clicked x value is smaller than any other -> one x value has exactly one y value
                if clicked_x > self.x[-1]:
                    # draw line between the two selected points
                    plt.plot([clicked_x, self.x[-1]], [clicked_y, self.y[-1]], 'bo', linestyle="-")
                    self.x += [clicked_x]
                    self.y += [clicked_y]
                else:
                    print('not possible')
            self.fig.canvas.draw()

    def _on_window_close(self, event):
        return self._get_fct_values()

    def _get_fct_values(self):
        return self.x, self.y


class FunctionApproximator:
    def __init__(self, fct_values: tuple):
        super().__init__()
        self.fct_values = fct_values

        fig = plt.figure(figsize=(12, 5))
        # ax1 for all degrees up to degree
        # ax2 only highest degree
        ax1, ax2 = fig.add_subplot(121), fig.add_subplot(122)

        # grid setup
        plt.xlim(0, 1)
        plt.ylim(-5, 5)
        plt.xlabel("X")
        plt.ylabel("Y")

        # draw fct to approximate
        ax1.plot(self.fct_values[0], self.fct_values[1])
        ax2.plot(self.fct_values[0], self.fct_values[1])

        # adapt
        smoothness = 0.01
        degree = 5

        x, f, L = self._plot_approximation(smoothness)

        # coefficients
        a0, a, b = self._discrete_fourier_transformation(smoothness, L, degree, x, f)
        f2 = None
        # draw approximation in range of degree
        for k in range(1, degree + 1):
            f2 = self._func_from_factors(x, L, a0, a, b, k)
            ax1.plot(x, f2, label=f'degree: {k}')
        ax1.legend()

        plt.title('Function Approximation')
        ax1.set_title(f'different degrees up to degree {degree}')
        ax2.set_title(f'degree: {degree}')

        # draw max degree approximation in 2nd ax
        ax2.plot(x, f2)

        plt.grid()

        plt.show()

    def _plot_approximation(self, dx):
        interp_data = interpolate.interp1d(self.fct_values[0], self.fct_values[1])

        new_data = ([], [])
        max_val, min_val = max(self.fct_values[0]), min(self.fct_values[0])
        L = (max_val - min_val) / 2.0

        for x_val in np.arange(min_val, max_val, dx * L):
            new_data[0].append(x_val)
            new_data[1].append(interp_data(x_val))
        return np.array(new_data[0]), np.array(new_data[1]), L

    def _func_from_factors(self, x, L, A0, A, B, n):
        fFS = A0 / 2
        for k in range(n):
            fFS = fFS + A[k] * np.cos((k + 1) * np.pi * x / L) + B[k] * np.sin((k + 1) * np.pi * x / L)
        return fFS

    def _discrete_fourier_transformation(self, dx, L, n, x, f):
        A = np.zeros(n)
        B = np.zeros(n)

        A0 = np.sum(f * np.ones_like(x)) * dx
        for k in range(n):
            A[k] = np.sum(f * np.cos(np.pi * (k + 1) * x / L)) * dx
            B[k] = np.sum(f * np.sin(np.pi * (k + 1) * x / L)) * dx
        return A0, A, B


if __name__ == '__main__':
    plotter = FunctionDrawer()
