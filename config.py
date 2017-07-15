import configparser as cp


class Config(object):
    def __init__(self):
        self.cfg = {}
        self.config = cp.RawConfigParser()
        self.config.read('preferences.cfg')

    def read(self):
        self.cfg = {
            'WINDOW': {
                'TITLE': self.config.get('Window', 'Title'),
                'HEIGHT': int(self.config.getint('Window', 'Height')),
                'WIDTH': int(self.config.getint('Window', 'Width')),
            },

            'DRAWING': {
                'BACKGROUND': self.config.get('Drawing', 'Background'),
                'LINES': self.config.get('Drawing', 'Lines'),
                'ALIVE_CELLS': self.config.get('Drawing', 'Alive'),
                'DELAY': float(self.config.getfloat('Drawing', 'Delay')),
            },

            'CA': {
                'N_CELLS': self.config.getint('CA', 'N'),
                'M_CELLS': self.config.getint('CA', 'M'),
                'ALIVE_CELLS_FILE': self.config.get('CA', 'Alive'),
                'ALIVE_CELLS': [],
            }
        }

        with open(self.cfg['CA']['ALIVE_CELLS_FILE'], 'r') as f:
            for i, line in enumerate(f):
                i, j = line.split(' ')
                self.cfg['CA']['ALIVE_CELLS'].append((int(i), int(j)))

        return self.cfg

    def write(self, cells):
        with open(self.cfg['CA']['ALIVE_CELLS_FILE'], 'w') as f:
            for cell in cells:
                f.write(str(cell[0]) + ' ' + str(cell[1]) + '\n')

