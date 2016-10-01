from . base import Component


class Grid(Component):
    template = "cba/layouts/grid.html"


class Column(Component):
    template = "cba/layouts/column.html"
    WIDTH = ["love", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine", "ten", "eleven", "twelve", "thirteen",
             "fourteen", "fifteen", "sixteen"]

    def __init__(self, id=None, width=16, *args, **kwargs):
        super(Column, self).__init__(id, *args, **kwargs)
        self.width = self.WIDTH[width]


class Row(Component):
    template = "cba/layouts/row.html"


class Split(Component):
    template = "cba/layouts/split.html"

    def __init__(self, id=None, direction="vertical", *args, **kwargs):
        super(Split, self).__init__(id, *args, **kwargs)
        self.direction = direction
