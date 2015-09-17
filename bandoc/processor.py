from copy import copy

from bandoc.model import MATRIX_SIZE, Sample

__author__ = 'mmatczuk'


class Processor(object):
    @staticmethod
    def get_max_region(samples):
        m0, m1 = MATRIX_SIZE, 0
        for s in samples:
            c0, c1 = Processor._get_region(s)
            if c0 < m0:
                m0 = c0
            if c1 > m1:
                m1 = c1

        return (m0, m1)

    @staticmethod
    def _get_region(sample):
        """
        For a given sample return Y-axis boundaries where high pressure values are.
        """
        total = 0.
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                total += sample.values[i][j]
        avg = total / (MATRIX_SIZE * MATRIX_SIZE)

        def is_row_good(row):
            return (sum(sample.values[row]) / MATRIX_SIZE) > avg

        for a in range(MATRIX_SIZE):
            if is_row_good(a):
                break

        for b in reversed(range(MATRIX_SIZE)):
            if is_row_good(b):
                break

        assert a < b, '%s, %s\n%s' % (a, b, sample)

        return (a, b)

    @staticmethod
    def clip_to_region(region, samples):
        r0, r1 = region
        for s in samples:
            del s.values[0:r0]
            del s.values[r1 - r0 + 1:]
            l = len(s.values)
            if l % 2 != 0:
                s.values.insert(l / 2 + 1, copy(s.values[l / 2]))

    # @staticmethod
    # def _interpolate_linear(sample, row):
    #     res = []
    #     for i in range(MATRIX_SIZE):
    #         res.append((sample.values[row][i] + sample.values[row + 1][i]) / 2)
    #     return res

    @staticmethod
    def split_avg(samples):
        joined_sample = Sample()
        del joined_sample.values[0:MATRIX_SIZE - len(samples[0].values)]

        for s in samples:
            for i in range(len(s.values)):
                for j in range(MATRIX_SIZE):
                    joined_sample.values[i][j] += s.values[i][j]

        multi = len(samples)

        l = len(joined_sample.values)
        count = (l / 2) * 4
        return {
            'q1': Processor._sum(joined_sample, l, l / 2, -2, 2) / (count * multi),
            'q2': Processor._sum(joined_sample, l, l / 2, 2, 6) / (count * multi),
            'q3': Processor._sum(joined_sample, l, l / 2, 6, 10) / (count * multi),
            'q4': Processor._sum(joined_sample, l, l / 2, 10, 14) / (count * multi),
            'q5': Processor._sum(joined_sample, l / 2, 0, -2, 2) / (count * multi),
            'q6': Processor._sum(joined_sample, l / 2, 0, 2, 6) / (count * multi),
            'q7': Processor._sum(joined_sample, l / 2, 0, 6, 10) / (count * multi),
            'q8': Processor._sum(joined_sample, l / 2, 0, 10, 14) / (count * (count * multi)),

            'prm': Processor._sum(joined_sample, l, l / 2, 2, 14) / (3 * count * multi),
        }

    @staticmethod
    def _sum(sample, t, b, l, r):
        total = 0.
        for i in range(b, t):
            for j in range(l, r):
                total += sample.values[i][j]

        return total
