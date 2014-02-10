'''
Implement a quadtree
'''
import geom_utils as gu


class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax):
        Node(xmin, ymin, xmax, ymax)
        tree.newnode(xmin, ymin, xmax, ymax)

    def insertsource(node, source):
        quadrant = newnode()

        if node.contents.length == MAX:
            subdivide(node)

        if node.q1 != None:
            if source.ximg >= node.xmid:
                if source.yimg >= node.ymid:
                    quadrant = node.q1
                else:
                    quadrant = node.q4
            else:
                if source.yimg >= node.ymid:
                    quadrant = node.q2
                else:
                    quadrant = node.q3

            insertsource(quadrant, source)

        else:
        # If no subquads exist add source to the list in CONTENTS element
            node.contents.append(source)

    def subdivide(node):
        node.q1 = new_node(node.xmid, node.ymid, node.box.xmax, node.box.ymax)
        node.q2 = new_node(node.box.xmin, node.ymid, node.xmid, node.box.ymax)
        node.q3 = new_node(node.box.xmin, node.box.ymin, node.xmid, node.ymid)
        node.q4 = new_node(node.xmid, node.box.ymin, node.box.xmax, node.ymid)

        # pop the list and insert the sources as they come off
        while node.contents:
            insertsource(node, node.contents.pop())

    def nearestsource(tree, x, y):
        # Initalize a box of interest
        dist = gu.dblmin(tree.box.xmax - tree.box.xmin, tree.box.ymax - tree.box.ymin)
        interest.xmin = x - dist
        interest.ymin = x - dist
        interest.xmax = x + dist
        interest.ymax = x + dist
        gu.clip_box(interest, tree.box)
        dist = dist * dist

        # How to keep track of nearest now?
        nearer_source(tree, tree, x, y, interest, nearest,  dist)

    def nearersource(tree, node, x, y, interest, nearest, dist):
        if gu.interestecting(node.box, interest):
            if node.q1 == None:
                for s in node.contents():
                    s_dist = norm(s.ximg, s.yimg, x, y)
                    if (s_dist < dist):
                        nearest = s
                        dist = s_dist

                        s_dist = sqrt(s_dist)
                        interest.xmin = x - s_dist
                        interest.ymin = y - s_dist
                        interest.xmax = x + s_dist
                        interest.ymax = y + s_dist
                        gu.clip_box(interest, tree.box)
            else:
                nearer_source(tree, node.q1, x, y, interest, nearest, dist)
                nearer_source(tree, node.q2, x, y, interest, nearest, dist)
                nearer_source(tree, node.q3, x, y, interest, nearest, dist)
                nearer_source(tree, node.q4, x, y, interest, nearest, dist)

class Box:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

class Node:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.box = Box(xmin, ymin, xmax, ymax )
        self.xmid = (xmin + xmax)/2
        self.ymid = (ymin + ymax)/2
        self.contents = []
