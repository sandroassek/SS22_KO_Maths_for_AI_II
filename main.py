from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt


class FunctionPlotter:
    def __init__(self):
        self.x = []
        self.y = []
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)

        plt.xlim(-10, 10)
        plt.ylim(-5, 5)
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.grid()

        plt.connect('button_press_event', self._on_mouse_click)
        self.fig.canvas.mpl_connect('close_event', self._on_window_close)

        plt.show()

    def _on_mouse_click(self, event):
        if event.button is MouseButton.RIGHT:
            clicked_x, clicked_y = event.xdata, event.ydata
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
        print(self._get_fct_values())
        self._get_fct_values()

    def _get_fct_values(self):
        return self.x, self.y

if __name__ == "__main__":
    plotter = FunctionPlotter()
    # print(plotter._get_fct_values())
