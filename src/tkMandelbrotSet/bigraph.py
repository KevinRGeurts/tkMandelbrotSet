"""
This python module defines classes for representing a bigraph data structure.

Exported classes:
    BigraphNode: Class that represents a node in a bigraph data structure.
    Bigraph: Class represents a bigraph data structure.
    Branch: Class represents a branch in a bigraph data structure.


Exported functions:
    None

Exported exceptions:
    None
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
        :parameter payload: data store for this node in the bigraph, any object
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
        """
        Return the unique ID of the node, as UUID.
        """
        return self._node_ID
    
    @property
    def predecessor(self):
        """
        Return the predecessor node of this node, as BigraphNode object. None if this node has no predecessor.
        """
        return self._predecessor

    @predecessor.setter
    def predecessor(self, value):
        """
        Set the predecessor node of this node.
        :parameter value: Predecessor bigraph node, as BigraphNode object
                          Note: value=None can be used to indicate that this node has no predecessor.
        """
        if value is not None:
            assert(isinstance(value, BigraphNode))
            assert(id(value)!=id(self)) # So we never get a loop
        self._predecessor = value

    def get_successors(self):
        """
        Return a list of this nodes' successor nodes.
        :return: List of successor nodes, as [BigraphNode objects]
        """
        return list(self._successors)

    def remove_successors(self):
        """
        Remove all the successors of the node. Those successor's predecessor will be set to None.
        :return: None
        """
        # First, each successor must have it's predecessor set to None, so that the successors don't continue to
        # link back to this node.
        for suc in self._successors:
            suc.predecessor = None
        # Second, clear this node's successor list.
        self._successors.clear()
        return None

    @property
    def successor(self):
        """
        Returns the first BigraphNode object in the list of successors of this BigraphNode. If there are no
        successors, then return None.
        Thus it handles the typical case of one successor only.
        :return: First successor node of this node, as BigraphNode object
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
        """
        Return this node's "payload" or data object, as any object.
        :return: Node's payload, as any object
        """
        return self._payload

    @payload.setter
    def payload(self, value):
        """
        Set this node's "payload" or data object.
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
        """
        Return the root node of this bigraph.
        :return: The root node of this bigraph, as BigraphNode object
        """
        return self._root

    @property
    def branches(self):
        """
        Return a list of the branches in the bigraph data structure, as [Branch objects]
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
        result = []
        current_node = root
        if current_node is not None:
            result.append(current_node)
            for suc in current_node.get_successors():
                result += self.traverse(suc)
        return result

    def prune(self, node=None):
        """
        Prune the tree by removing all nodes from parameter node successor(s) out to and including the tip nodes of all
        successive branches. Thus parameter node will become the new tip of the branch. If the node has multiple successors,
        that is, if the branch split's to form more branches, all branches above the current node will be "pruned off".
        
        Note: The branch that will be retained will be the first branch that contains the parameter node. 
        
        :parameter node: The node above which the pruning will occur, as BigraphNode object
        :return: None
        """
        assert(isinstance(node, BigraphNode))
        # Determine all the branches in the graph which containe the parameter node. Only one of these branches will be retained
        # in the tree when the prunning is done.
        pruned_branches = []
        for br in self._branches:
            if br.is_node_on_branch(node):
                pruned_branches.append(br)
        # Do the pruning
        if len(pruned_branches) > 0:
            pruned_branches[0].prune(node)
        # Eliminate any orphaned branches from the graph
        if len(pruned_branches) > 1:
            for i in range(1,len(pruned_branches)):
                br = pruned_branches[i]
                br._tip_node = None # To enable BigraphNode garbage collection
                self._branches.remove(br)
        return None

    def __getitem__(self, index):
        """
        Return the branch index-th branch in the bigraph, as Branch object
        :parameter index: Selects which branch to get, as integer
        :return: Index-th branch in the bigraph, as Branch object
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
        """
        Get the unique ID of the branch.
        :return: Unique branch ID, as UUID
        """
        return self._branch_ID
        
    @property
    def name(self):
        """
        Get the name of the branch.
        :return: Branch name, as string
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the name of the branch.
        :parameter value: The new branch name, as string
        """
        assert(type(value)==str)
        self._name = value

    @property
    def tip_node(self):
        """
        Get the tip node of the branch.
        :return: Tip node of branch, as BigraphNode object
        """
        return self._tip_node

    @tip_node.setter
    def tip_node(self, value):
        """
        Set the tip node of the branch.
        :parameter value: Branch's new tip node, as BigraphNode object.
        """
        assert(isinstance(value, BigraphNode))
        self._tip_node = value

    def prune(self, node=None):
        """
        Prune the branch by removing all nodes from parameter node successor(s) out to and including the tip node of the
        branch. Thus parameter node will become the new tip of the branch. If the node has multiple successors, that is,
        if the branch split's to form more branches, all branches above the current node will be "pruned off".
        :parameter node: The node above which the pruning will occur, as BigraphNode object
        :return: None
        """
        assert(isinstance(node, BigraphNode))
        # If parameter node IS the tip node of the branch, then do nothing.
        if self.tip_node != node:
            # Store parameter node's successors, for later use
            sucs = node.get_successors()
            # Remove node's successors, to start the prune
            node.remove_successors()
            # Set tip node of branch to parameter node
            self.tip_node = node
            # This completes the pruning operation as far as the remaining branch goes.
            # What remains to be done is to set to None the predecessors and successors of all the pruned off nodes,
            # so that the nodes can be garbage collected. (Otherwise, since successors reference predecessors which reference
            # successors, the pruned off nodes will never be garbage collected.)
            for suc in sucs:
                # Use Bigraph classes' traverse() method to create a list of all nodes above each successor in the tree
                pruned_nodes = Bigraph().traverse(suc)
                for pn in pruned_nodes:
                    pn.predecessor = None
                    pn.remove_successors()
        return None
        
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
        Return the number of nodes in the branch, as integer.
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
        Return the subsript-th node in the branch, where 0=tip node of the branch, as BigraphNode object.
        The tip node of the branch is node 0.
        :parameter subscript: Selects the node to return from the branch, as integer
        :return: Subscript-th node in the branch, as BigrahNode object
        """
        if type(subscript)!=int: raise TypeError
        if subscript > (len(self)-1): raise IndexError
        current_node = self.tip_node
        for i in range(len(self)):
            if i == subscript:
                return current_node
            current_node = current_node.predecessor
