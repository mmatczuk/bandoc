__author__ = 'mmatczuk'

MATRIX_SIZE = 16


class Sample(object):
    def __init__(self):
        self.values = []
        for i in range(MATRIX_SIZE):
            self.values.append([0.] * MATRIX_SIZE)

    def __repr__(self):
        s = []
        for cols in reversed(self.values):
            s.append(' '.join(map(lambda x: '%06.2f' % x, cols)))
        return '\n'.join(s)
