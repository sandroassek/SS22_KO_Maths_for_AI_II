import numpy as np
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt


class FunctionPlotter:
    def __init__(self):
        self.x = []
        self.y = []
        self.fig = plt.figure()
        self.fig

        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.grid()

        plt.connect('button_press_event', self._on_mouse_click)
        self.fig.canvas.mpl_connect('close_event', self._on_window_close)
        plt.show()

    def _on_mouse_click(self, event):
        if event.button is MouseButton.LEFT:
            clicked_x, clicked_y = event.xdata, event.ydata
            if len(self.x) == 0 and len(self.y) == 0:
                self.x += [clicked_x]
                self.y += [clicked_x]
                plt.plot(clicked_x, clicked_y, 'bo')
            else:
                curr_x = self.x[-1]
                # check if new clicked x value is smaller than any other
                if clicked_x > curr_x:
                    self.x += [clicked_x]
                    self.y += [clicked_x]
                    plt.plot(clicked_x, clicked_y, 'bo')
                else:
                    print('not possible')
            self.fig.canvas.draw()

    def _on_window_close(self, event):
        print(self._get_fct_values())
        self._get_fct_values()

    def _get_fct_values(self):
        return self.x, self.y


plotter = FunctionPlotter()
# print(plotter._get_fct_values())
