from . import colors


DEFAULT_X_STEP = 1
DEFAULT_Y_STEP = 1

DEFAULT_X_DELTA = 10
DEFAULT_Y_DELTA = 10

DEFAULT_AXPREC = (0, 0)

DEFAULT_X_TICKS_MAX = 1000
DEFAULT_Y_TICKS_MAX = 1000
DEFAULT_Y0_TICKS = 5 / 2 # == (Высота шрифта, мм) / 2
DEFAULT_DELIM = ","

DEFAULT_CHART_LINE_STYLE = 1

RANDOM_COLOR = -1

class Chart:
    def __init__(
            self,
            bridge,
            step = None,
            xlims = None,
            ylims = None,
            rdim = None,
            axprec = DEFAULT_AXPREC,
            view_name = None):

        self.bridge = bridge
        self.bridge.init({
            "view_name": view_name,
        })

        self.x_step = step[0]
        self.y_step = step[1]

        if (self.x_step <= 0):
            print("x_step <= 0")
            self.x_step = DEFAULT_X_STEP

        if (self.y_step <= 0):
            print("y_step <= 0")
            self.y_step = DEFAULT_Y_STEP

        self.x_min, self.x_max = xlims
        self.y_min, self.y_max = ylims

        if (self.x_min > self.x_max):
            print("x_min > x_max")
            self.x_min, self.x_max = self.x_max, self.x_min

        if (self.y_min > self.y_max):
            print("y_min > y_max")
            self.y_min, self.y_max = self.y_max, self.y_min

        self.x_delta = self.x_max - self.x_min
        self.y_delta = self.y_max - self.y_min

        if (self.x_delta == 0):
            print("x_delta == 0")
            self.x_delta = DEFAULT_X_DELTA

        if (self.y_delta == 0):
            print("y_delta == 0")
            self.y_delta = DEFAULT_Y_DELTA

        self.x_rdim, self.y_rdim = rdim

        # коэффициент пропорциональности
        self.x_k = self.x_rdim / self.x_delta
        self.y_k = self.y_rdim / self.y_delta

        # x real step
        self.x_rstep = self.x_step * self.x_k
        self.y_rstep = self.y_step * self.y_k

        self.x_rmax = self.x_max * self.x_k
        self.x_rmin = self.x_min * self.x_k

        self.y_rmax = self.y_max * self.y_k
        self.y_rmin = self.y_min * self.y_k

        self.x_rdelta = self.x_rmax - self.x_rmin
        self.y_rdelta = self.y_rmax - self.y_rmin

        # axis ticks precision
        self.x_axprec, self.y_axprec = axprec
        self.x_axprecf = "{{:.{}f}}".format(self.x_axprec)
        self.y_axprecf = "{{:.{}f}}".format(self.y_axprec)


    def background(self):
        self.bridge.macro_start("background")

        self.frame()
        self.grid()

        self.bridge.macro_end("background")


    def frame(self):
        rect = self.bridge.draw_rect(
            0, 0, self.x_rdelta, self.y_rdelta,
        )
        self.bridge.macro_add("background", rect)


    def grid(self):
        x_ticks = int(self.x_delta / self.x_step) + 1
        if (x_ticks == 0):
            print("x_ticks == 0")
        if (x_ticks > DEFAULT_X_TICKS_MAX):
            print("x_ticks > DEFAULT_X_TICKS_MAX")
            x_ticks = DEFAULT_X_TICKS_MAX

        y_ticks = int(self.y_delta / self.y_step) + 1
        if (y_ticks == 0):
            print("y_ticks == 0")
        if (y_ticks > DEFAULT_Y_TICKS_MAX):
            print("y_ticks > DEFAULT_Y_TICKS_MAX")
            y_ticks = DEFAULT_Y_TICKS_MAX


        self.bridge.macro_start("x_ticks")
        self.bridge.macro_start("y_ticks")
        # вдоль оси x
        for i in range(x_ticks):
            xi = i * self.x_rstep
            line = self.bridge.draw_line(xi, 0, xi, self.y_rdelta, 2)
            self.bridge.macro_add("background", line)

            tick = self.x_min + i * self.x_step
            str = self.x_axprecf.format(tick).replace(".", DEFAULT_DELIM)
            text = self.bridge.draw_text(xi, -10, str)
            self.bridge.macro_add("x_ticks", text)

        # вдоль оси y
        for j in range(y_ticks):
            yj = j * self.y_rstep
            line = self.bridge.draw_line(0, yj, self.x_rdelta, yj, 2)
            self.bridge.macro_add("background", line)

            tick = self.y_min + j * self.y_step
            str = self.y_axprecf.format(tick).replace(".", DEFAULT_DELIM)
            text = self.bridge.draw_text(-10, yj - DEFAULT_Y0_TICKS, str)
            self.bridge.macro_add("y_ticks", text)

        self.bridge.macro_end("x_ticks")
        self.bridge.macro_end("y_ticks")


    def plot(self, x, y, name = "plot", color = colors.RANDOM):
        x_r = x * self.x_k - self.x_rmin
        y_r = y * self.y_k - self.y_rmin
        xypairs = zip(x_r, y_r)
        x1, y1 = next(xypairs)

        self.bridge.macro_start(name, to_layer = True, color = color)
        for xi, yi in xypairs:
            x2 = xi
            y2 = yi

            line = self.bridge.draw_line(x1, y1, x2, y2, DEFAULT_CHART_LINE_STYLE)
            self.bridge.macro_add(name, line)

            x1 = x2
            y1 = y2

        self.bridge.macro_end(name)
