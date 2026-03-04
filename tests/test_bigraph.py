"""
This module contains unit tests for the BigraphNode class.
"""


# standard library imports
import unittest
from uuid import UUID


# local imports
from tkMandelbrotSet.bigraph import BigraphNode, Branch, Bigraph


class Test_BigraphNode(unittest.TestCase):
    def test_init_property_getters(self):
        pre = BigraphNode(payload=1)
        suc = BigraphNode(payload=2)
        node = BigraphNode(predecessor=pre, successor=suc, payload=3)
        self.assertEqual(pre.payload, node.predecessor.payload)
        self.assertEqual(suc.payload, node.successor.payload)
        self.assertTrue(type(node.nodeID)==UUID)

    def test_successor_property_setter(self):
        suc = BigraphNode(payload=1)
        node = BigraphNode()
        node.successor = suc
        self.assertEqual(suc, node.successor)
        # Now try to add suc again, which should not happen
        node.successor = suc
        self.assertEqual(1, len(node._successors))
        # Add a second, unique successor to node
        suc2 = BigraphNode(payload=2)
        node.successor = suc2
        self.assertEqual(2, len(node._successors))
        # Getter should still get the first successor added
        self.assertEqual(suc, node.successor)

    def test_get_successors(self):
        suc = BigraphNode(payload=1)
        node = BigraphNode()
        node.successor = suc
        # Add a second, unique successor to node
        suc2 = BigraphNode(payload=2)
        node.successor = suc2
        exp_val = [suc, suc2]
        act_val = node.get_successors()
        self.assertListEqual(exp_val, act_val)

    def test_predecessor_property_setter(self):
        pre = BigraphNode(payload=1)
        node = BigraphNode()
        node.predecessor = pre
        self.assertEqual(pre, node.predecessor)

    def test_payload_property_setter(self):
        node = BigraphNode()
        node.payload = 1
        self.assertEqual(1, node.payload)

    def test_insert_node_after_True_once(self):
        node1 = BigraphNode(payload=1)
        node2 = BigraphNode(payload=2)
        node1.insert_node(new_node=node2, after=True)
        # chain should now look like (from beginning to end): node1->node2
        # node2 should have no successor, since it is the last node of the chain
        self.assertEqual(None, node2.successor)
        # node1 should be the predecessor of node2
        self.assertEqual(node1, node2.predecessor)
        # node2 should be the successor of node1
        self.assertEqual(node2, node1.successor)
        # node1 should have no predecessor, as it is the first node of the chain
        self.assertEqual(None, node1.predecessor)

    def test_insert_node_after_True_twice(self):
        node1 = BigraphNode(payload=1)
        node2 = BigraphNode(payload=2)
        node1.insert_node(new_node=node2, after=True)
        node3 = BigraphNode(payload=3)
        node1.insert_node(new_node=node3, after=True)
        # chain should now look like (from beginning to tip): node1->node3->node2
        # node2 should have no successor, since it is the last node of the chain
        self.assertEqual(None, node2.successor)
        # node3 should be the predecessor of node2
        self.assertEqual(node3, node2.predecessor)
        # node2 should be the successor of node3
        self.assertEqual(node2, node3.successor)
        # node1 should be the predecessor of node3
        self.assertEqual(node1, node3.predecessor)
        # node3 should be the successor of node1
        self.assertEqual(node3, node1.successor)
        # node1 should have no predecessor, as it is the first node of the chain
        self.assertEqual(None, node1.predecessor)

    def test_insert_node_after_False_once(self):
        node1 = BigraphNode(payload=1)
        node2 = BigraphNode(payload=2)
        node1.insert_node(new_node=node2, after=False)
        # chain should now look like (from beginning to end): node2->node1
        # node1 should have no successor, since it is the last node of the chain
        self.assertEqual(None, node1.successor)
        # node2 should be the predecessor of node1
        self.assertEqual(node2, node1.predecessor)
        # node1 should be the successor of node2
        self.assertEqual(node1, node2.successor)
        # node2 should have no predecessor, as it is the first node of the chain
        self.assertEqual(None, node2.predecessor)

    def test_insert_node_after_False_twice(self):
        node1 = BigraphNode(payload=1)
        node2 = BigraphNode(payload=2)
        node1.insert_node(new_node=node2, after=False)
        node3 = BigraphNode(payload=3)
        node1.insert_node(new_node=node3, after=False)
        # chain should now look like (from beginning to tip): node2->node3->node1
        # node1 should have no successor, since it is the last node of the chain
        self.assertEqual(None, node1.successor)
        # node3 should be the predecessor of node1
        self.assertEqual(node3, node1.predecessor)
        # node1 should be the successor of node3
        self.assertEqual(node1, node3.successor)
        # node2 should be the predecessor of node3
        self.assertEqual(node2, node3.predecessor)
        # node3 should be the successor of node2
        self.assertEqual(node3, node2.successor)
        # node2 should have no predecessor, as it is the first node of the chain
        self.assertEqual(None, node2.predecessor)


class Test_Branch(unittest.TestCase):
    def test_init_property_getters(self):
        node = BigraphNode(payload=1)
        _name = 'branch 1'
        branch = Branch(tip=node, name=_name)
        self.assertEqual(_name, branch.name)
        self.assertEqual(node, branch.tip_node)
        self.assertTrue(type(branch.branchID)==UUID)

    def test_name_property_setter(self):
        branch = Branch(name='')
        _name = 'branch 1'
        branch.name = _name
        self.assertEqual(_name, branch.name)

    def test_tip_node_property_setter(self):
        _tip = BigraphNode(payload=1)
        branch = Branch()
        branch.tip_node = _tip
        self.assertEqual(_tip, branch.tip_node)

    def test_add_node_len(self):
        tip1 = BigraphNode(payload=1)
        branch = Branch(tip=tip1)
        tip2 = BigraphNode(payload=2)
        tip3 = BigraphNode(payload=3)
        branch.add_node(node=tip2)
        branch.add_node(node=tip3)
        # Branch should now look like (from beginning to tip): tip1->tip2->tip3
        # tip3 should be the branches' tip node
        self.assertEqual(tip3, branch.tip_node)
        # tip3 should have no successor, since it is the tip node of the branch
        self.assertEqual(None, branch.tip_node.successor)
        # tip2 should be the prdecessor tip3 (the branches' tip node)
        self.assertEqual(tip2, branch.tip_node.predecessor)
        # tip2's successoer should be tip3
        self.assertEqual(tip3, tip2.successor)
        # tip2's predecessor should be tip1
        self.assertEqual(tip1, tip2.predecessor)
        # tip1's successor should be tip2
        self.assertEqual(tip2, tip1.successor)
        # tip1 should not have a prdecessor
        self.assertEqual(None, tip1.predecessor)

    def test_len(self):
        tip1 = BigraphNode(payload=1)
        branch = Branch(tip=tip1)
        tip2 = BigraphNode(payload=2)
        tip3 = BigraphNode(payload=3)
        branch.add_node(node=tip2)
        branch.add_node(node=tip3)
        # Branch should now look like (from beginning to tip): tip1->tip2->tip3
        # should have 3 nodes in the branch
        self.assertEqual(3, len(branch))

    def test_getitem(self):
        tip1 = BigraphNode(payload=1)
        branch = Branch(tip=tip1)
        tip2 = BigraphNode(payload=2)
        tip3 = BigraphNode(payload=3)
        branch.add_node(node=tip2)
        branch.add_node(node=tip3)
        # Branch should now look like (from beginning to tip): tip1->tip2->tip3
        # branch[0] should be tip3, etc
        self.assertEqual(tip3, branch[0])
        self.assertEqual(tip2, branch[1])
        self.assertEqual(tip1, branch[2])
        # Now test some exceptions
        self.assertRaises(IndexError, branch.__getitem__, 3)
        self.assertRaises(TypeError, branch.__getitem__, 'not an integer')

    def test_is_node_on_branch(self):
        tip1 = BigraphNode(payload=1)
        branch = Branch(tip=tip1)
        tip2 = BigraphNode(payload=2)
        tip3 = BigraphNode(payload=3)
        branch.add_node(node=tip2)
        branch.add_node(node=tip3)
        # Branch should now look like (from beginning to tip): tip1->tip2->tip3
        self.assertTrue(branch.is_node_on_branch(tip2))
        nonbranch_node = BigraphNode(payload=4)
        self.assertFalse(branch.is_node_on_branch(nonbranch_node))


class Test_Bigraph(unittest.TestCase):
    def test_init_property_getters(self):
        node = BigraphNode(payload=1)
        graph = Bigraph(root=node)
        self.assertEqual(node, graph.root)

    def test_add_branch_at_root_len_getitem(self):
        graph = Bigraph()
        branch1 = Branch(name='branch1')
        branch2 = Branch(name='branch2')
        graph.add_branch(new_branch=branch1)
        graph.add_branch(new_branch=branch1) # Should do nothing. Can't add same branch twice.
        graph.add_branch(new_branch=branch2)
        self.assertEqual(2, len(graph))
        self.assertEqual(branch1, graph[0])
        self.assertEqual(branch2, graph[1])

    def test_add_branch_not_at_root_len_getitem(self):
        graph = Bigraph()
        branch1 = Branch(name='branch1')
        node1 = BigraphNode(payload=1)
        branch1.add_node(node1)
        graph.add_branch(new_branch=branch1)
        # branch1: graph.root -> (branch1 original tip node) -> node1 
        branch2 = Branch(name='branch2')
        graph.add_branch(at_node=node1, new_branch=branch2)
        # branch2: graph.root -> (branch1 original tip node) -> node1 -> branch2.tip_node
        self.assertEqual(2, len(graph))
        self.assertEqual(branch1, graph[0])
        self.assertEqual(branch2, graph[1])
        self.assertEqual(node1, branch1[0])
        self.assertEqual(node1, branch2[1])

    def test_traverse(self):
        graph = Bigraph()
        branch1 = Branch(name='branch1')
        tip1 = branch1.tip_node
        node1 = BigraphNode(payload=1)
        branch1.add_node(node1)
        graph.add_branch(new_branch=branch1)
        # branch1: graph.root -> (branch1 original tip node) -> node1 
        branch2 = Branch(name='branch2')
        graph.add_branch(at_node=node1, new_branch=branch2)
        # branch2: graph.root -> (branch1 original tip node) -> node1 -> branch2.tip_node
        graph_nodes = graph.traverse(graph.root)
        self.assertEqual(4, len(graph_nodes))
        exp_val = [graph.root, tip1, node1, branch2.tip_node]
        self.assertListEqual(exp_val, graph_nodes)

    def test_get_nodes_branch(self):
        graph = Bigraph()
        branch1 = Branch(name='branch1')
        tip1 = branch1.tip_node
        node1 = BigraphNode(payload=1)
        branch1.add_node(node1)
        graph.add_branch(new_branch=branch1)
        # branch1: graph.root -> (branch1 original tip node) -> node1 
        branch2 = Branch(name='branch2')
        graph.add_branch(at_node=node1, new_branch=branch2)
        # branch2: graph.root -> (branch1 original tip node) -> node1 -> branch2.tip_node
        self.assertEqual(branch2, graph.get_nodes_branch(branch2.tip_node))
        # Test that a node shared amongst branches belongs to the first branch it is shared by.
        self.assertEqual(branch1, graph.get_nodes_branch(node1))
        # Test a node that isn't in the graph
        nongraph_node = BigraphNode(payload=2)
        self.assertEqual(None, graph.get_nodes_branch(nongraph_node))


if __name__ == '__main__':
    unittest.main()
