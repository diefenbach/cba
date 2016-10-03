from . base import Component


class Grid(Component):
    """A CSS grid layout.

    A grid consists arbitrary rows and 16 columns per row. see http://semantic-ui.com/collections/grid.html
    for more.
    """
    template = "cba/layouts/grid.html"


class Column(Component):
    """A column of a grid.

        width
            The width of the column. Valid values are 1-16. A row consist of
            maxmimal 16 columns but can be ended explicitly.
    """
    template = "cba/layouts/column.html"
    WIDTH = ["love", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine", "ten", "eleven", "twelve", "thirteen",
             "fourteen", "fifteen", "sixteen"]

    def __init__(self, id=None, width=16, *args, **kwargs):
        super(Column, self).__init__(id, *args, **kwargs)
        self.width = self.WIDTH[width]


class Row(Component):
    """A row of a grid.

    It can be used to end a row explicitly.
    """
    template = "cba/layouts/row.html"


class Split(Component):
    """Splits the screen in two or more panels.

    All direct sub components are splitted into an own panel. Split components
    can be nested.

        direction
            The direction of the splitting. One of ``vertical`` or ``horizontal``.
    """
    template = "cba/layouts/split.html"

    def __init__(self, id=None, direction="vertical", *args, **kwargs):
        super(Split, self).__init__(id, *args, **kwargs)
        self.direction = direction
