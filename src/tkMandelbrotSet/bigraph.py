"""
This python module defines classes for representing a bigraph data structure.
"""

# standard imports
from uuid import uuid4

# local imports



class BigraphNode(object):
    """
    This class represents a node in a bigraph data structure.
    """
    def __init__(self, predecessor=None, successor=None, payload=None):
        """
        :parameter predecssor: predessor node in the bigraph, BigraphNode object
        :parameter successor: successor node in the bigraph, BigraphNode object
        :parameter payload: data store for this node in the bigraph, any Object
        """
        # Create a unique ID for the node
        self._node_ID = uuid4()
        
        if predecessor is not None:
            assert(isinstance(predecessor, BigraphNode))
        self._predecessor = predecessor

        self._successors=[]
        if successor is not None:
            assert(isinstance(successor, BigraphNode))
            self._successors.append(successor)
        
        self._payload = payload

    def __str__(self):
        result = f"BigraphNode {id(self)}: payload={self.payload}, predecessor={id(self.predecessor)}, successor[0]={id(self.successor)}."
        return result

    @property
    def nodeID(self):
        return self._node_ID
    
    @property
    def predecessor(self):
        return self._predecessor

    @predecessor.setter
    def predecessor(self, value):
        """
        :parameter value: Predecessor bigraph node, as BigraphNode object
        """
        if value is not None:
            assert(isinstance(value, BigraphNode))
        self._predecessor = value

    @property
    def successor(self):
        """
        Returns the first BigraphNode object in the list of successors of this BigraphNode. If there are no
        successors, then return None.
        Thus it handles the typical case of one successor only.
        """
        if len(self._successors)>0:
            return self._successors[0]
        else:
            return None

    @successor.setter
    def successor(self, value):
        """
        Add a successor to the bigraph node if it isn't already a successor of the bigraph node.
        :parameter value: Successor bigraph node, as BigraphNode object
        """
        if value is not None:
            assert(isinstance(value, BigraphNode))
            if value not in self._successors:
                self._successors.append(value)

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        """
        :parameter value: Bigraph node data, as any object
        """
        self._payload = value


class Bigraph(object):
    """
    This class represents a bigraph data structure.
    """
    def __init__(self, root=BigraphNode()):
        """
        :parameter root: The root node of the bigraph structure, as BigraphNode object
        """
        assert(isinstance(root, BigraphNode))   
        self._root = root
        self._branches = []

    @property
    def root(self):
        return self._root

    @property
    def branches(self):
        """
        Return a list of the branches in the bigraph data structure, as [Branch]
        """
        return list(self._branches)

    def add_branch(self, value):
        """
        Add a branch to the bigraph if it isn't already a branch of the bigraph.
        :parameter value: Branch to add to the bigraph, as Branch object
        """
        if value is not None:
            assert(isinstance(value, Branch))
            if value not in self._branches:
                self._branches.append(value)

    def __getitem__(self, index):
        """
        Return the branch index-th branch in the bigraph, as Branch object
        """
        return self._branches[index]

    def __len__(self):
        """
        Return the number of branches in the bigraph, as int
        """
        return len(self._branches)        


class Branch(BigraphNode):
    """
    This class represents a branch in a bigraph structure.
    """
    def __init__(self, tip=BigraphNode(), name=''):
        """
        :parameter tip: The bigraph node at the tip of this branch, as BigraphNode object
        :parameter name: The name of this branch, as string
        """
        assert(isinstance(tip, BigraphNode))
        self._tip_node = tip
        assert(type(name)==str)
        self._name =name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert(type(value)==str)
        self._name = value

    @property
    def tip_node(self):
        return self._tip_node

    @tip_node.setter
    def tip_node(self, value):
        assert(isinstance(value, BigraphNode))
        self._tip_node = value

    def insert_node(self, node=BigraphNode(), tip=False):
        """
        Insert a node into the bigraph branch.
        :parameter node: The node to insert into the branch, as BigraphNode object
        :parameter tip: If True, then the inserted node becomes the new tip, with the old tip becoming it's predecessor.
                        If False, then the inserted node becomes the predecessor of the tip node, and it's predecessor
                        is the tip's previous predecessor.
        :return None:
        """
        assert(isinstance(node, BigraphNode))
        assert(type(tip)==bool)
        if tip:
            old_tip = self.tip_node
            old_tip.successor = node
            self.tip_node = node
            self.tip_node.predecessor = old_tip
        else:
            # The current tip node's predecessor is going to get pushed down
            if self.tip_node.predecessor is not None:
                self.tip_node.predecessor.successor = node
            node.successor = self.tip_node
            node.predecessor = self.tip_node.predecessor
            self.tip_node.predecessor = node
        return None
