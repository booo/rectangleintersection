#!/usr/bin/env python2


# make sure you install shapely, matplotlib and descartes
# maybe you want to use a virtual environment
# virtualenv env && . env/bin/activate
# pip install shapely matplotlib descartes

from shapely.geometry import Polygon

from matplotlib import pyplot
from descartes import PolygonPatch

from intervaltree import Leaf, Interval


# deprecated implementation

class IntervalTree(object):

    def __init__(self):
        self.center = None
        self.intervals = []
        self.left = None
        self.right = None


    def insert(self, interval):
        min, max = interval
        if not self.center:
            #tree is empty
            self.center = (min + max) / 2.0
            self.intervals = [interval]

        else:
            if max < self.center:
                if not self.left:
                    self.left = IntervalTree()
                self.left.insert(interval)

            elif min > self.center:
                if not self.right:
                    self.right = IntervalTree()
                self.right.insert(interval)
            else:
                self.intervals.append(interval)

    #FIXME I'm a stupid function
    def remove(self, interval):
        min, max = interval

        try:
            self.intervals.remove(interval)
            if len(self.intervals) is 0 and not self.left and not self.right:
                #remove subtree/node
                return True
        except ValueError:
            pass

        if self.left and min <= self.center:
            if self.left.remove(interval):
                self.left = None

        if self.right and max >= self.center:
            if self.right.remove(interval):
                self.right = None

    def find(self, interval):
        min, max = interval
        #TODO increase readability
        overlapping = [i for i in self.intervals if i[1] >= min and i[0] <= max]

        if self.left and min <= self.center:
            overlapping += self.left.find(interval)

        if self.right and max >= self.center:
            overlapping += self.right.find(interval)

        return overlapping


#tree = IntervalTree()
#tree.insert((0,1))
#tree.insert((0.75,2))
#print tree.find((0,1))
##tree.insert((0,1))
#tree.remove((0.75,2))

class Rectangle(object):

    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def get_y_interval(self):
        return Interval(self.miny, self.maxy, self)

    def get_x_interval(self):
        return Interval(self.minx, self.maxx, self)

    def get_polygon(self):
        return Polygon(
                ((self.minx, self.miny),
                (self.maxx, self.miny),
                (self.maxx, self.maxy),
                (self.minx, self.maxy),
                (self.minx, self.miny)
                ))

    def get_events(self):
        return [(self.minx, 'start', self), (self.maxx,'end', self)]


def rectangle_intersection(rectangles):
    events = []
    intersections = []
    #intervalTree = IntervalTree()
    intervalTree = Leaf()

    for rectangle in rectangles:
       events = events + rectangle.get_events()

    #sort events by x
    events = sorted(events, key=lambda event: event[0])

    for x, type, rectangle in events:
        if type is 'end':
            #remove y interval from interval tree
            intervalTree = intervalTree.remove(rectangle.get_y_interval())
        else:
            #1) check for intersection
            for intersection in intervalTree.search(rectangle.get_y_interval()):
                intersections.append((rectangle, intersection.value))
            #2) insert into interval tree
            intervalTree = intervalTree.insert(rectangle.get_y_interval())

    return intersections


# testing
rectangles = [Rectangle(90,40,110,70),
Rectangle(10,40,40,70),
Rectangle(75,60,95,80),
Rectangle(30,20,60,50),
Rectangle(100,20,130,50),
Rectangle(70,10,85,40)
]

print rectangle_intersection(rectangles)

figure = pyplot.figure()
ax = figure.add_subplot(111)

BLUE = '#6699cc'

for rectangle in rectangles:
    patch = PolygonPatch(rectangle.get_polygon(), fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
    ax.add_patch(patch)

ax.set_title('rectangle intersection')
ax.axis('equal')
pyplot.show()
