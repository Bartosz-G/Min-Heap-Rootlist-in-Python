


#Breath-First-ish like algorithmm that Finds the first empty node, used for attaching in linkheaps (returns that node)
#(checks by height to ensure efficient attaching in linkHeaps)
def _firstEmptyNode(r,A):
    if not A:
        A.append(r)

    temp = []
    for i in range(0,len(A)):
        if type(A[i]) != Node:
            raise ValueError('the function requires a Node to be passed as an argument')
        if A[i].left is None:
            return A[i]
        if A[i].right is None:
            return A[i]
        temp.append(A[i].left)
        temp.append(A[i].right)

    return _firstEmptyNode(r,temp)


#Quickfix for a bug where repeated calling of the algorithm caused it to take A value from the previous calls
# -instead of an empty list at any first iteration
def firstEmptyNode(r):
    return _firstEmptyNode(r,[])


#Heapify's a single node with it's children, used for a buildMinHeap
def minHeapify (r):
    if type(r) != Node:
        raise ValueError('the argument ',r,' passed to the function is not a Node')
    elif r.left is None and r.right is None:
        return

    Smallest = r

    if r.left is not None and Smallest.value > r.left.value:
        Smallest = r.left

    if r.right is not None and Smallest.value > r.right.value:
        Smallest = r.right

    temp1 = r.value
    temp2 = Smallest.value

    if Smallest == r:
        return
    elif Smallest == r.left:
        r.left.value = temp1
        r.value = temp2
        minHeapify(r.left)
    elif Smallest == r.right:
        r.right.value = temp1
        r.value = temp2
        minHeapify(r.right)
    else:
        raise ValueError('Unknown error from handling:',Smallest)


#Breath-First-ish like algorithmm that Finds all the nodes and stores the pointers to them in list sorted by
# -their height, starting from r (root) in A[0]
def _findAllNodes(r,A):
    if not A:
        A.append([r])

    current = A[-1]
    next = []

    for i in range(0,len(current)):
        if type(current[i]) != Node:
            raise ValueError('the function requires a Node to be passed as an argument')
        if current[i].left is None and current[i].right is None:
            continue

        if current[i].left is not None:
            next.append(current[i].left)

        if current[i].right is not None:
            next.append(current[i].right)

    if not next:
        return A

    A.append(next)
    return _findAllNodes(r,A)


#Quickfix for a bug where repeated calling of the algorithm caused it to take A value from the previous calls
# -instead of an empty list at any first iteration
def findAllNodes(r):
    return _findAllNodes(r,[])


#Takes the root of a tree and heapifies the entire tree, returns the root again.
def buildMinHeap(r):
    if type(r) != Node:
        raise ValueError('the argument ',r,' passed to the function is not a Node')

    A = findAllNodes(r).copy()

    while A:
        current = A.pop(-1)
        for i in range(0,len(current)):
            minHeapify(current[i])

    return r










class Node:
    def __init__(self, val, le, ri, pa):
        self.value = val
        self.left = le
        self.right = ri
        self.parent = pa



    def print(self):
        self.printrec(0)

    # recursively prints the values in the tree, indenting by depth
    def printrec(self,depth):
        print("    "*depth,end="") # right amount of indentation
        print(self.value)
        if self.left==None:
            print("    "*(depth+1),"None")
        else:
            self.left.printrec(depth+1)
        if self.right==None:
            print("    "*(depth+1),"None")
        else:
            self.right.printrec(depth+1)




class Item:
    def __init__(self, aroot, p, n):
        self.heap = aroot
        self.previous = p
        self.next = n

class MinHeaplist:
    def __init__(self):
        self.min = None

    def insert(self, x):
        if type(x) == int:
            n = Node(x,None,None,None)
        elif type(x) == Node:
            #The algorithm accepts nodes with children on purpose, simplifies the .decreaseKey and .union later
            if x.parent != None:
                raise ValueError('insert() method requires a root to be inputted')
            else:
                n = x
        else:
            raise ValueError('Not a valid input')

        if self.min is None:
            temp = Item(n,None,None)
            self.min = temp
            self.min.next = self.min
            self.min.previous = self.min

        else:
            if self.min.heap.value < n.value:
                #Push it in front of min
                temp = Item(n,self.min,self.min.next)
                self.min.next.previous = temp
                self.min.next = temp
            else:
                #Push min one place further
                temp = Item(n,self.min.previous,self.min)
                self.min.previous.next = temp
                self.min.previous = temp
                #Replace current min with the new one
                self.min = temp

    #My own method, that simplifies clean-up operations and union
    #Simply removes the next item (opposite of insert) and outputs a root, (will take out entire min-heaps if it
    # - encounters such, used for union and clean-up)
    def remove(self):
        if self.min is None:
            raise ValueError('Cannot remove from an empty root list')

        if self.min.next == self.min:
            raise ValueError('Cannot remove min value, try extractMin()')

        temp = self.min.next

        self.min.next.next.previous = self.min
        self.min.next = self.min.next.next

        return temp.heap

    def linkheaps(self, h1, h2):
        if type(h1) != Node:
            raise ValueError('the argument ', h1, ' passed to the function is not a Node')
        if type(h2) != Node:
            raise ValueError('the argument', h2 ,' passed to the function is not a Node')

        if h1.parent is not None:
            raise ValueError('the argument ', h1, ' cannot have a parent')
        if h1.parent is not None:
            raise ValueError('the argument', h2 ,' cannot have a parent')

        attach = None

        #Checks which value is smaller and places it at the top, the other one get's attached to wherever first empty -
        # -node has been found by firstEmptyNode(h) operation
        if h1.value < h2.value:
            attach = firstEmptyNode(h1)
            if attach.left is None:
                attach.left = h2
                h2.parent = attach
            elif attach.right is None:
                attach.right = h2
                h2.parent = attach
            else:
                raise ValueError('Unknown error from handling: ',attach)

            return buildMinHeap(h1)

        else:
            attach = firstEmptyNode(h2)
            if attach.left is None:
                attach.left = h1
                h1.parent = attach
            elif attach.right is None:
                attach.right = h1
                h1.parent = attach
            else:
                raise ValueError('Unknown error from handling: ',attach)

            return buildMinHeap(h2)

    def extractMin(self):
        min = self.min.heap

        if min.left is not None and min.right is not None:
            lchild = min.left
            rchild = min.right
            min.left = None
            min.right = None
            lchild.parent = None
            rchild.parent = None
            newroot = self.linkheaps(lchild,rchild)
            self.min.heap = newroot
        elif min.left is not None and min.right is None:
            lchild = min.left
            lchild.parent = None
            min.left = None
            self.min.heap = lchild
        elif min.left is None and min.right is not None:
            rchild = min.right
            rchild.parent = None
            min.right = None
            self.min.heap = rchild
        else:
            if self.min.next == self.min:
                self.min = None
                return min
            else:
                #Push next into min
                tempnext = self.min.next
                tempnext.previous = self.min.previous
                self.min.previous.next = tempnext
                self.min = tempnext

        #Clean-up
        while self.min.next != self.min:
            current = self.min.heap
            nextroot = self.remove()
            newroot = self.linkheaps(current,nextroot)
            self.min.heap = newroot

        #Returns a node, not just it's value
        return min

    def decreaseKey(self, node, k):
        if type(node) != Node:
            raise ValueError('the argument ', node, ' passed to the function is not a Node')

        if node.value < k:
            raise ValueError('this method cannot increase Nodes value')

        if node == self.min.heap:
            self.min.heap.value = k
            return


        if self.min.heap.value > k and node.parent is None:
            #Case 1. Swaps the old min with new key (this way the algorithm doesn't have to circle through the list and
            # - swap the elements, preserving the O(1) requirement, min-heaps are preserved bcs k < old min < n's old value)
            oldmin = self.min.heap.value
            self.min.heap.value = k
            node.value = oldmin
        elif self.min.heap.value <k and node.parent is None:
            #Case 2. Simply change node's value to the new key, as we're decreasing the key, the min-heap will be preserved
            node.value = k
        else:
            #case 3. Disconnect it from the parent and .insert() with new key value (.insert() will replace new min if needed))
            oldParent = node.parent
            if oldParent.left == node:
                oldParent.left = None
            else:
                oldParent.right = None
            node.parent = None
            node.value = k
            self.insert(node)



    def union(self, H):
        #The exercise doesn't explicitly state whether .union() was meant to combine the min-heaps of both heap-lists
        # -or just re-insert Items
        #This is the execution for the first case but second one can be simply done by copying clean-up from extractMin
        # -and pasting it after 341 line
        if type(H) != MinHeaplist:
            raise ValueError('the argument ', H, ' passed to the function is not a MinHeapList')

        while H.min.next != H.min:
            temp = H.remove()
            self.insert(temp)

        temp2 = H.min.heap
        self.insert(temp2)
        H.min = None

    def print(self):
        h=self.min
        if h != None:
            print("-----")
            h.heap.print()
            h = h.next
            while h != self.min:
                print("-----")
                h.heap.print()
                h = h.next
            print("-----")



if __name__ == '__main__':
    print("--------- Tests provided by the lecturer ----------")
    H = MinHeaplist()

    print("Inserting 5")
    H.insert(5)
    print("Inserting 3")
    H.insert(3)
    print("Inserting 7")
    H.insert(7)
    print("Inserting 6")
    H.insert(6)
    H.print()

    print("Extracting ", H.extractMin().value)

    print("The current min-heaplist:")
    H.print()

    print("Inserting 4")
    H.insert(4)

    print("The current min-heaplist:")
    H.print()

    n = H.min.next.heap.left
    print("Decreasing key", n.value, "to 2")
    H.decreaseKey(n, 2)
    H.print()
    print("Extracting min: ",H.extractMin().value)
    H.print()

    print("--------- My own additional tests ----------")
    L = MinHeaplist()
    L.insert(10)
    L.insert(7)
    L.insert(3)
    L.insert(14)
    L.insert(5)
    print("Printing L before the decrease key")
    L.print()

    print("Decreasing:", L.min.next.next.heap.value, " to :", 2)
    L.decreaseKey(L.min.next.next.heap, 2)
    print("After DecreaseKey")
    L.print()

    K = MinHeaplist()
    K.insert(12)
    K.insert(4)
    K.insert(8)
    K.insert(18)
    print("Printing K")
    K.print()

    L.union(K)
    print("Printing the union")
    L.print()
    print("Extracting min value:", L.extractMin().value)
    L.print()
    print("Extracting min value:", L.extractMin().value)
    print(
        "Not sure whether the .print shows it correctly but if you check the nodes manually the min-heaps are preserved")
    L.print()
    print("Extracting min value:", L.extractMin().value)
    L.print()
    extract = L.min.heap.left.left
    print("We're decreasing:", extract.value, "to 3")
    L.decreaseKey(extract, 3)
    L.print()
    print("Extracting min value:", L.extractMin().value)
    print("Extracting min value:", L.extractMin().value)
    print("Extracting min value:", L.extractMin().value)
    L.print()
    print("Extracting min value:", L.extractMin().value)
    print("Extracting min value:", L.extractMin().value)
    print("Extracting min value:", L.extractMin().value)
    print("Is the minheaplist empty? :",L.min is None)
