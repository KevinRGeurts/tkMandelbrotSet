"""
This python module defines classes for representing a bigraph data structure.
"""

# standard imports
from uuid import uuid4
from xml.sax.handler import property_declaration_handler

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
            assert(id(value)!=id(self)) # So we never get a loop
        self._predecessor = value

    def get_successors(self):
        """
        Return a list of this nodes' successor nodes.
        :return: [successor nodes]
        """
        return list(self._successors)

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
            assert(id(value)!=id(self)) # So we never get a loop
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

    def insert_node(self, new_node, after=True):
        """
        Insert a new node at the this node.
        :parameter new_node: The new BigraphNode object to insert, as BigraphNode object.
        :parameter after: If after=True, the insert new_node as successor of this node. Otherwise insert it as predecessor. As bool.
        :return: None
        """
        if new_node is not None:
            assert(isinstance(new_node, BigraphNode))
            if after:
                # new_node is to be inserted AFTER this node
                for s in self._successors:
                    # new_node's successors must be set to this node's successors
                    new_node.successor = s
                    # the predecessor of this node's successors must be set to new_node
                    s.predecessor = new_node
                # new_node's predecessor must be set to this node
                new_node.predecessor = self
                # this node's successor is now ONLY new_node
                self._successors.clear()
                self.successor = new_node
                # this node's predecessor is unchanged
            else:
                # new_node is to be inserted BEFORE this node
                # the predecessor of this node must have this node removed from its successors and new_node added to its successors
                if self.predecessor is not None:
                    self.predecessor._successors.remove(self)
                    self.predecessor.successor = new_node
                # new_node's successor must be set to this node
                new_node.successor = self
                # new_node's predecessor must be set to this node's predecessor
                new_node.predecessor = self.predecessor
                # this node's predecessor must be set to new_node
                self.predecessor = new_node
                # this node's successors are not changed
        return None


class Bigraph(object):
    """
    This class represents a bigraph data structure.
    """
    def __init__(self, root=None):
        """
        :parameter root: The root node of the bigraph structure, as BigraphNode object
        """
        if root is None:
            # Create a new unique node for the root of the graph
            root = BigraphNode()
        else:
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

    def add_branch(self, at_node=None, new_branch=None):
        """
        Add a branch to the bigraph if it isn't already a branch of the bigraph.
        :parameter at_node: Node at which to add the new branch, as BigraphNode object
                            If at_node=None, then new branch is added at the bigraph's root node.
        :parameter new_branch: Branch to add to the bigraph, as Branch object
        :return: None
        """
        if new_branch is not None:
            assert(isinstance(new_branch, Branch))
            if new_branch not in self._branches:
                self._branches.append(new_branch)
                if at_node is not None:
                    assert(isinstance(at_node, BigraphNode))
                    # tip node of new branch must be added to successors of at_node
                    at_node.successor = new_branch.tip_node
                    # predecessor of tip node of new branch must be set to at_node
                    new_branch.tip_node.predecessor = at_node
                else:
                    # "base" node of new branch must be added to successors of graph's root node
                    self.root.successor = new_branch[len(new_branch)-1]
                    # predecessor of "base" node of new branch must be set to graph's root node
                    new_branch[len(new_branch)-1].predecessor = self.root
        return None

    def get_nodes_branch(self, node):
        """
        Return the branch that parameter node belongs to in the graph. Note that since a node can belong to more than
        one branch, depending on its location relative to splits in a branch, for purposes of this method,
        such a node will belong to the first branch it belonged to.
        :parameter node: The node for which the owning branch is requested, as BigraphNode object
        :return: The branch of the graph the node belongs to, as Branch object
                 Note: Returns None if node is not an any branch in the graph.
        """
        assert(isinstance(node, BigraphNode))
        result = None
        for br in self._branches:
            if br.is_node_on_branch(node):
                result = br
                break
        return result

    def traverse(self, root=None):
        """
        Traverse the bigraph "upwards" (i.e., from root to tips), visiting each node, and returning a list of nodes.
        :parameter root: The node of the bigraph at which to start the traverse, as BigraphNode object
        :return: List of nodes in the bigraph, as [BigraphNode objects]
        """
        # result = []
        # current_node = root
        # while current_node is not None:
        #     result.append(current_node)
        #     for suc in current_node.get_successors():
        #         result += self.traverse(suc)
        # return result
        result = []
        current_node = root
        if current_node is not None:
            result.append(current_node)
            for suc in current_node.get_successors():
                result += self.traverse(suc)
        return result

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
    def __init__(self, tip=None, name=''):
        """
        :parameter tip: The bigraph node at the tip of this branch, as BigraphNode object
        :parameter name: The name of this branch, as string
        """
        # Create a unique ID for the branch
        self._branch_ID = uuid4()
        
        if tip is None:
            # Create a new unique node for the tip
            tip = BigraphNode()
        else:
            assert(isinstance(tip, BigraphNode))
        self._tip_node = tip
        assert(type(name)==str)
        self._name =name

    @property
    def branchID(self):
        return self._branch_ID
        
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

    def add_node(self, node=None):
        """
        Add a node at the tip of the bigraph branch.
        :parameter node: The node to insert at the tip of the branch, as BigraphNode object
        :return None:
        """
        if node is None:
            # Create a new unique node to add
            node = BigraphNode()
        else:
            assert(isinstance(node, BigraphNode))
        self.tip_node.insert_node(node)
        self.tip_node = node
        return None

    def is_node_on_branch(self, node):
        """
        Determine if parameter node is on this branch.
        :parameter node: The node to check the branch for, as BigraphNode
        :return: True if parameter node is on this branch, otherwise False, as boolean
        """
        assert(isinstance(node, BigraphNode))
        result = False
        for node_index in range(len(self)):
            if self[node_index].nodeID == node.nodeID:
                result = True
                break
        return result

    def __len__(self):
        """
        Return the number of nodes in the branch.
        """
        num_nodes = 0
        at_root = False
        current_node = self.tip_node
        assert(current_node is not None)
        while not at_root:
            num_nodes += 1
            current_node = current_node.predecessor
            if current_node is None:
                at_root = True
        return num_nodes

    def __getitem__(self, subscript):
        """
        Return the subsript-th node in the branch, where 0=tip node of the branch, as Branch object
        """
        if type(subscript)!=int: raise TypeError
        if subscript > (len(self)-1): raise IndexError
        current_node = self.tip_node
        for i in range(len(self)):
            if i == subscript:
                return current_node
            current_node = current_node.predecessor
