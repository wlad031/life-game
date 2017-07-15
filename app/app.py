import time
from app.utils import *

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

DEAD = 0
ALIVE = 1


class CA(object):
    class Cell(object):
        def __init__(self, pos_i, pos_j, state):
            self.pos_i = pos_i
            self.pos_j = pos_j
            self.state = state

    class Neighbor(object):
        def __init__(self, offset_i, offset_j):
            self.offset_i = offset_i
            self.offset_j = offset_j

        def __eq__(self, o):
            return self.offset_i == o.offset_i and self.offset_j == o.offset_j

    def __init__(self, n, m, default_state=0):
        self.n = n
        self.m = m
        self.rules = []
        self.default_state = default_state
        self.cells = self.reset()

    def reset(self):
        return list(
            [list([CA.Cell(i, j, self.default_state)
                   for j in range(self.m)])
             for i in range(self.n)])

    def update(self):
        new_cells = []
        for h in self.cells:
            new_cells.append([])
            for c in h:
                new_cells[-1].append(CA.Cell(c.pos_i, c.pos_j, c.state))
                for rule in self.rules:
                    if rule.verify(c, self.cells):
                        new_cells[c.pos_i][c.pos_j].state = rule.result_state
        self.cells = new_cells

    def __str__(self):
        s = ''
        for h in self.cells:
            for c in h:
                s += str(c.state)
            s += '\n'
        return s


class Rule(object):
    def __init__(self, current_state, result_state, neighbors, fun,
                 cyclic=False):
        self.current_state = current_state
        self.result_state = result_state
        self.neighbors = neighbors
        self.fun = fun
        self.cyclic = cyclic

    def __extract_neighbor_cells(self, cell, all_cells):
        ls = []
        n, m = len(all_cells), len(all_cells[0])

        for neighbor in self.neighbors:
            i = cell.pos_i + neighbor.offset_i
            j = cell.pos_j + neighbor.offset_j

            if not self.cyclic:
                if i < 0 or j < 0 or i >= n or j >= m:
                    continue
            else:
                i = i % n
                j = j % m

            ls.append(all_cells[i][j])

        return ls

    def verify(self, cell, all_cells):
        if cell.state != self.current_state:
            return False

        neighbor_cells = self.__extract_neighbor_cells(cell, all_cells)
        return self.fun(neighbor_cells)


class Life(object):
    def __init__(self, n, m):
        self.ca = CA(n, m, default_state=DEAD)

        r = range(-1, 2)
        neighbors = list([CA.Neighbor(i, j) for i in r for j in r])
        neighbors.remove(CA.Neighbor(0, 0))

        def foo(neighbor_cells):
            return len(
                list(filter(lambda cell: cell.state == ALIVE, neighbor_cells)))

        self.ca.rules = [
            Rule(current_state=DEAD, result_state=ALIVE, neighbors=neighbors,
                 cyclic=False, fun=lambda nc: foo(nc) == 3),
            Rule(current_state=ALIVE, result_state=ALIVE, neighbors=neighbors,
                 cyclic=False, fun=lambda nc: foo(nc) in [2, 3]),
            Rule(current_state=ALIVE, result_state=DEAD, neighbors=neighbors,
                 cyclic=False, fun=lambda nc: foo(nc) in [0, 1, 4, 5, 6, 7, 8]),
        ]


class CADrawer(object):

    def __init__(self, ca, cfg, config):
        self.ca = ca
        self.cfg_o = cfg
        self.config = config

        self.__EXIT = False
        self.__PAUSE = True

        self.root = Tk()
        self.root.title(self.config['WINDOW']['TITLE'])
        self.root.resizable(0, 0)
        self.canvas = Canvas(self.root,
                             width=self.config['WINDOW']['WIDTH'],
                             height=self.config['WINDOW']['HEIGHT'])

        self.canvas.pack()

        self.root.bind("<Button-1>", self.__click)
        self.root.bind('p', self.__push_p)
        self.root.bind('s', self.__push_s)
        self.root.bind('<Escape>', self.__push_esc)
        self.root.bind('<Return>', self.__push_enter)
        self.root.protocol("WM_DELETE_WINDOW", self.__close)

        self.__DEFAULT_ANIMATION_DELAY = self.config['DRAWING']['DELAY']

        self.root.after(0, self.__animation)
        self.root.mainloop()

    def __update_elements(self):
        self.canvas.delete('cell')

        width, height = self.config['WINDOW']['WIDTH'], \
                        self.config['WINDOW']['HEIGHT']
        n, m = self.ca.n, self.ca.m
        step_i, step_j = height / n, width / m

        for i in range(n):
            self.__create_line((0, i * step_i), (500, i * step_i))
        for j in range(m):
            self.__create_line((j * step_j, 0), (j * step_j, 500))

        for row in self.ca.cells:
            for cell in row:
                self.__create_rectangle(
                    (cell.pos_i * step_i, cell.pos_j * step_j),
                    ((cell.pos_i + 1) * step_i, (cell.pos_j + 1) * step_j),
                    color=(self.config['DRAWING']['ALIVE_CELLS']
                           if cell.state == ALIVE
                           else self.config['DRAWING']['BACKGROUND']))

    def __animation(self):
        width, height = self.config['WINDOW']['WIDTH'], \
                        self.config['WINDOW']['HEIGHT']
        n, m = self.ca.n, self.ca.m
        step_i, step_j = height / n, width / m

        for i in range(n):
            self.__create_line((0, i * step_i), (width, i * step_i))
        for j in range(m):
            self.__create_line((j * step_j, 0), (j * step_j, height))

        self.__update_elements()
        while True:
            if self.__EXIT:
                break

            time.sleep(self.__DEFAULT_ANIMATION_DELAY)

            if not self.__PAUSE:
                self.ca.update()
                self.__update_elements()

            self.canvas.update()

    def __click(self, event):
        width, height = self.config['WINDOW']['WIDTH'], \
                        self.config['WINDOW']['HEIGHT']
        n, m = self.ca.n, self.ca.m
        step_i, step_j = height / n, width / m

        i, j = int(event.x / step_i), int(event.y / step_j)
        self.ca.cells[i][j].state = ALIVE \
            if self.ca.cells[i][j].state == DEAD else DEAD
        self.__update_elements()

    def __push_esc(self, event):
        self.__EXIT = True
        self.root.withdraw()
        sys.exit(0)

    def __push_p(self, event):
        self.__PAUSE = not self.__PAUSE

    def __push_s(self, event):
        self.cfg_o.write(
            list(map(lambda x: (x.pos_i, x.pos_j),
                     filter(lambda x: x.state == ALIVE,
                            flatten(self.ca.cells)))))

    def __push_enter(self, event):
        if self.__PAUSE:
            self.ca.update()
            self.__update_elements()

    def __close(self):
        self.__push_esc(None)

    def __create_line(self, x1, x2):
        return self.canvas.create_line(
            x1[0], x1[1], x2[0], x2[1],
            fill=self.config['DRAWING']['LINES'])

    def __create_rectangle(self, x1, x2, color):
        return self.canvas.create_rectangle(
            x1[0], x1[1], x2[0], x2[1],
            fill=color,
            tags='cell')


class Runner(object):
    @staticmethod
    def run(cfg, data):
        life = Life(data['CA']['N_CELLS'], data['CA']['M_CELLS'])

        for x in data['CA']['ALIVE_CELLS']:
            life.ca.cells[x[0]][x[1]].state = ALIVE

        CADrawer(life.ca, cfg, data)
