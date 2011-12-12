class Node:
    def __init__(self,value):

        self.left = Leaf()
        self.right = Leaf()
        self.value = value
        self.maxima = value.high

    def search(tree,interval):
        if interval.low > tree.maxima:
            return []
        elif interval.high < tree.value.low:
            return tree.left.search(interval)
        else:
            intersects = []

            if interval.intersects(tree.value):
                intersects.append(tree.value)

            intersects.extend(tree.left.search(interval))
            intersects.extend(tree.right.search(interval))

            return intersects

    def insert(tree,interval):
        if interval.high > tree.maxima:
            tree.maxima = interval.high

        if tree.value.low >= interval.low:
            tree.left = tree.left.insert(interval)
        else:
            tree.right = tree.right.insert(interval)

        return tree

    def remove(tree,interval):

        if interval == tree.value:
            if isinstance(tree.left,Leaf):
                return tree.right
            elif isinstance(tree.right,Leaf):
                return tree.left
            else:
                # find in order predecessor
                pre, newLeftTree = tree._returnAndRemoveMax(tree.left)
                tree.left = newLeftTree
                tree.value = pre
                tree.maxima = max(tree.right.maxima,tree.value.high,tree.left.maxima)
                return tree

        elif interval.low < tree.value.low:
            tree.left = tree.left.remove(interval)
            tree.maxima = max(tree.right,tree.left,tree.value.high)
            return tree
        else:
            tree.right = tree.right.remove(interval)
            tree.maxima = max(tree.right,tree.left,tree.value.high)
            return tree

    def _returnAndRemoveMax(tree):
        if not isinstance(tree.right,Leaf):
            rightValue,RemTree = tree.right._returnAndRemoveMax()
            tree.right = RemTree

            tree.maxima = max(tree.right.maxima,max(tree.value.high,tree.left.maxima))

            return(rightValue,tree)
        else:
            return(tree.value,tree.left)

    def __str__(self):
        return ("(" + str(self.left) + "    " + str(self.value) + "|" +
        str(self.maxima) + "     " + str(self.right) + ")")

class Interval:
    def  __init__(self,left,right, value):
        self.low = left
        self.high = right
        self.value = value

    def intersects(self,other):
        if(self.high < other.low):
            return False
        elif(other.high < self.low):
            return False
        else:
            return True

    def __str__(self):
        return str((self.low,self.high)) + " | " + str(self.value)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.low is other.low and self.high is other.high


class Leaf(Node):

    def __init__(self):
        self.maxima = 0

    def __str__(self):
        return("nil")

    def search(self,_interval):
        return []

    def insert(self,interval):
        return Node(interval)

    def remove(self, value):
        return self
