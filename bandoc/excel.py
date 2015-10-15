import re

from bandoc.model import Sample

__author__ = 'mmatczuk'


class Parser(object):
    def __init__(self, book, limit=20):
        self.__limit = limit
        self.__book = book
        self.__header_map = None
        self.__samples = []

    def samples(self):
        return self.__samples

    def parse(self):
        self._read_header()

        start = None
        header = True
        for _, cells in self.__book[1].rows().iteritems():
            if header:
                header = not header
                continue

            if start is None:
                start = self._get_value(cells[0].value)
            elif start + self.__limit < self._get_value(cells[0].value):
                break

            s = Sample()
            for cell in cells:
                self._handle_cell(cell, s)
            self.__samples.append(s)

        self.__book.close()

    def _handle_cell(self, cell, sample):
        v = self.__header_map[self._get_col_name(cell.id)]
        if not v:
            return

        (x, y) = v
        sample.values[x - 1][y - 1] = self._get_value(cell.value)

    def _read_header(self):
        self.__header_map = {
            self._get_col_name(cell.id): self._get_header_cords(cell.value) for cell in self.__book[1][1]
        }

    @staticmethod
    def _get_col_name(cell_id):
        return re.search(r'[A-Z]+', cell_id).group(0)

    @staticmethod
    def _get_header_cords(cell_header):
        if not isinstance(cell_header, tuple):
            return None
        return cell_header[3:5]

    @staticmethod
    def _get_value(str_value):
        return float(str_value.strip())
