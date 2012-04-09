""" 
file: sbbtree_heap.py
language: python3
author: mtf@cs.rit.edu Matthew Fluet
student author: Ethan Hale Jurman ehj2229@rit.edu
description: Heap implemented with size-balanced binary trees
"""

import random

class TreeNode( object ):
    """
       A (non-empty) binary tree node for a size-balanced binary tree heap.
       SLOTS:
         key: Orderable
         value: Any
         size: NatNum; the size of the sub-tree rooted at this node
         parent: NoneType|TreeNode; the parent node
         lchild: NoneType|TreeNode; the node of the left sub-tree
         rchild: NoneType|TreeNode; the node of the right sub-tree
    """
    __slots__ = ( 'key', 'value', 'size', 'parent', 'lchild', 'rchild' )

    def __init__( self, key, value, parent ):
        self.key = key
        self.value = value
        self.parent = parent
        self.lchild = None
        self.rchild = None
        self.size = 1

    def __str__( self ):
        slchild = str(self.lchild)
        srchild = str(self.rchild)
        skv = str((self.key, self.value)) + " <" + str(self.size) + ">"
        pad = " " * (len(skv) + 1)
        s = ""
        for l in str(self.lchild).split('\n'):
            s += pad + l + "\n"
        s += skv + "\n"
        for l in str(self.rchild).split('\n'):
            s += pad + l + "\n"
        return s[:-1]

class SBBTreeHeap( object ):
    """
       A size-balanced binary tree heap.
       SLOTS:
         root: NoneType|TreeNode
    """
    __slots__ = ( 'root' )

    def __init__( self ):
        self.root = None

    def __str__( self ):
        return str(self.root)

######################################################################
# Professors code
######################################################################
def checkNode( node, parent ):
    """
       checkNode: NoneType|TreeNode NoneType|TreeNode -> Tuple(NatNum, Boolean, Boolean, Boolean, Boolean)
       Checks that the node correctly records size information,
       correctly records parent information, satisfies the
       size-balanced property, and satisfies the heap property.
    """
    if node == None:
        return 0, True, True, True, True
    else:
        lsize, lsizeOk, lparentOk, lbalanceProp, lheapProp = checkNode( node.lchild, node )
        rsize, rsizeOk, rparentOk, rbalanceProp, rheapProp = checkNode( node.rchild, node )
        nsize = lsize + 1 + rsize
        nsizeOk = node.size == nsize
        sizeOk = lsizeOk and rsizeOk and nsizeOk
        nparentOk = node.parent == parent
        parentOk = lparentOk and rparentOk and nparentOk
        nbalanceProp = abs(lsize - rsize) <= 1
        balanceProp = lbalanceProp and rbalanceProp and nbalanceProp
        nheapProp = True
        if (node.lchild != None) and (node.lchild.key < node.key):
            nheapProp = False
        if (node.rchild != None) and (node.rchild.key < node.key):
            nheapProp = False
        heapProp = lheapProp and rheapProp and nheapProp
        return nsize, sizeOk, parentOk, balanceProp, heapProp

def checkHeap( heap ):
    """
       checkHeap: SBBTreeHeap -> NoneType
       Checks that the heap is a size-balanced binary tree heap.
    """
    __, sizeOk, parentOk, balanceProp, heapProp = checkNode( heap.root, None )
    if not sizeOk:
        print("** ERROR **  Heap nodes do not correctly record size information.")
    if not parentOk:
        print("** ERROR **  Heap nodes do not correctly record parent information.")
    if not balanceProp:
        print("** Error **  Heap does not satisfy size-balanced property.")
    if not heapProp:
        print("** Error **  Heap does not satisfy heap property.")
    assert(sizeOk and parentOk and balanceProp and heapProp)
    return

######################################################################
# END OF Professors code
######################################################################


def empty(heap):
    """
       empty: SBBTreeHeap -> Boolean
       Returns True if the heap is empty and False if the heap is non-empty.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Must be an O(1) operation.
    """
    ## COMPLETE empty FUNCTION ##
    if not isinstance(heap, SBBTreeHeap):
        raise TypeError("not a heap")
    if heap.root == None:
        return True
    else:
        return False

def enqueue( heap, key, value= None ):
    """
       enqueue: SBBTreeHeap Orderable Any -> NoneType
       Adds the key/value pair to the heap.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Must be an O(log n) operation.
    """
    ## COMPLETE enqueue FUNCTION ##
    
    if value == None:
        value = key

    if not isinstance( heap, SBBTreeHeap ):
        raise TypeError("not a heap")

    if heap.root == None:
        heap.root = TreeNode( key, value, None )

    else:
        nodeA = addNode( heap.root, key, value )
        return siftUp( nodeA )
    
def addNode( node, key, value ):
    node.size += 1
    if (node.size)%2 == 1:
        #go right
        if node.size == 3:
            node.rchild = TreeNode( key, value, node ); return node.rchild
        return addNode( node.rchild, key, value )
    else:
        if node.size == 2:
            node.lchild = TreeNode( key, value, node ); return node.lchild
        #go left
        return addNode( node.lchild, key, value )


def frontMin( heap ):
    """
       frontMin: SBBTreeHeap -> Tuple(Orderable, Any)
       Returns (and does not remove) the minimum key/value in the heap.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Raises IndexError if heap is empty.
       Precondition: not empty(heap)
       Must be an O(1) operation.
    """
    ## COMPLETE frontMin FUNCTION ##
    if not isinstance(heap, SBBTreeHeap):
        raise TypeError("TypeError fool!")
    if heap.root == None:
        raise IndexError("heap is empty!")
    else:
        return ( heap.root.key, heap.root.value )


def dequeueMin( heap ):
    """
       dequeueMin: SBBTreeHeap -> NoneType
       Removes (and does not return) the minimum key/value in the heap.
       Raises TypeError if heap is not an instance of SBBTreeHeap.
       Raises IndexError if heap is empty.
       Precondition: not empty(heap)
       Must be an O(log n) operation.
    """
    ## COMPLETE dequeueMin FUNCTION ##
  
    if not isinstance(heap, SBBTreeHeap):
        raise TypeError("not a heap")
    if empty(heap):
        heap.root = None
        return None
#    print("heap is not empty")
    if heap.root.size == 1:
        heap.root = None
        return None
    storeNode = removeNode( heap.root )
    heap.root.value = storeNode[0]
    heap.root.key = storeNode[1]
    return siftDn( heap.root )

def removeNode( node ):
    node.size -= 1
    if node.size%2 == 0:
        # go right
        if node.rchild == None:
            nodeV = node.value
            nodeK = node.key
            tple = (nodeV, nodeK)
            if node.parent.rchild == node:
                node.parent.rchild = None
            else:
                node.parent.lchild = None
            return tple
        return removeNode( node.rchild )
    else:
        # go left
        return removeNode( node.lchild )
    
  


def heapsort( l ):
    """
       heapsort: ListOfOrderable -> ListOfOrderable
       Returns a list that has the same elements as l, but in ascending order.
       The implementation must a size-balanced binary tree heap to sort the elements.
       Must be an O(n log n) operation.
    """
    ## COMPLETE heapsort FUNCTION ##
    heap = SBBTreeHeap()
    lst = []
    for element in l:
        enqueue(heap, element)
    while not empty(heap):
        front = frontMin(heap)
        lst.append(frontMin(heap)[0])
        dequeueMin(heap)
    return lst

def siftUp( node ):
    if node.parent == None:
#        print("at the top!")
        return
    if node.parent.key > node.key:
#        print("%s <-> %s" % (node.key, node.parent.key)) 
        switchNode( node, node.parent )
#        print("%s > %s?" % (node.key, node.parent.key))
#        print("")
        return siftUp( node.parent )
#    print("nodes are good! %s >= %s" % (node.key, node.parent.key))
    return

def siftDn( node ):
    nodeL = isinstance(node.lchild, TreeNode)
    nodeR = isinstance(node.rchild, TreeNode)
    
    if not nodeL and not nodeR:
#        print("reached the end of the heap")
        return None

    if nodeL and not nodeR:
        if node.lchild.key < node.key:
#            print("%s <-> %s" % (node.lchild.key, node.key))
#            print("%s > %s" % (node.lchild.key, node.key))
            switchNode( node.lchild, node )
            return siftDn( node.lchild )
        else:
#            print("no switch (%s < %s)" % (node.key, node.lchild.key))
            return None

    if nodeR and not nodeL:
        if node.rchild.key < node.key:
#            print("%s <-> %s" % (node.rchild.key, node.key))
#            print("%s > %s" % (node.rchild.key, node.key))
            switchNode( node.rchild, node )
            return siftDn( node.rchild )
        else:
#            print("no switch (%s < %s)" % (node.key, node.rchild.key))
            return None

    if nodeR and nodeL:
        if (node.rchild.key <= node.lchild.key) and (node.rchild.key < node.key): # if the right child < left child and if the right child is bigger the the parent
#            print("%s > %s" % (node.rchild.key, node.key))
            switchNode( node.rchild, node )
            return siftDn( node.rchild )
        if (node.lchild.key < node.rchild.key) and (node.lchild.key < node.key):# if the left child < right child and if the left child is bigger then the parent
#            print("%s < %s" % (node.lchild.key, node.key))
            switchNode( node.lchild, node )
            return siftDn( node.lchild )

        else:
#            print("good spot for a node")
            return None


def switchNode( node1, node2 ):
#    print("%s(%s) <-> %s(%s)" % (node1.value,node1.key, node2.value,node2.key))
    value1 = node1.value; key1 = node1.key; value2 = node2.value; key2 = node2.key
    node1.value = value2; node2.value = value1; node1.key = key2; node2.key = key1

    

######################################################################
# Professors code
######################################################################

if __name__ == "__main__":
    R = random.Random()
    R.seed(0)
    print(">>> h = SBBTreeHeap()");
    h = SBBTreeHeap()
    print(h)
    checkHeap(h)
    for v in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        k = R.randint(0,99)
        print(">>> enqueue(h," + str(k) + "," + str(v) + ")")
        enqueue(h, k, v)
        print(h)
        checkHeap(h)
    while not empty(h):
        print(">>> k, v = frontMin(h)")
        k, v = frontMin(h)
        print((k, v))
        print(">>> dequeueMin(h)")
        dequeueMin(h)
        print(h)
        checkHeap(h)
    for i in range(4):
        l = []
        for x in range(2 ** (i + 2)):
            l.append(R.randint(0,99))
        print(" l = " + str(l))
        sl = heapsort(l)
        print("sl = " + str(sl))

######################################################################
# END OF Professors code
######################################################################

