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

    def test_predecessor_property_setter(self):
        pre = BigraphNode(payload=1)
        node = BigraphNode()
        node.predecessor = pre
        self.assertEqual(pre, node.predecessor)

    def test_payload_property_setter(self):
        node = BigraphNode()
        node.payload = 1
        self.assertEqual(1, node.payload)


class Test_Branch(unittest.TestCase):
    def test_init_property_getters(self):
        node = BigraphNode(payload=1)
        _name = 'branch 1'
        branch = Branch(tip=node, name=_name)
        self.assertEqual(_name, branch.name)
        self.assertEqual(node, branch.tip_node)

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

    def test_insert_node_tip_True(self):
        tip1 = BigraphNode(payload=1)
        branch = Branch(tip=tip1)
        tip2 = BigraphNode(payload=2)
        tip3 = BigraphNode(payload=3)
        branch.insert_node(node=tip2, tip=True)
        branch.insert_node(node=tip3, tip=True)
        # Branch should now look like (from beginning to tip): tip1->tip2->tip3
        self.assertEqual(tip3, branch.tip_node)
        self.assertEqual(None, branch.tip_node.successor)
        self.assertEqual(tip2, branch.tip_node.predecessor)
        self.assertEqual(tip3, tip2.successor)
        self.assertEqual(tip1, tip2.predecessor)
        self.assertEqual(tip2, tip1.successor)
        self.assertEqual(None, tip1.predecessor)

    def test_insert_node_tip_False(self):
        tip1 = BigraphNode(payload=1)
        branch = Branch(tip=tip1)
        tip2 = BigraphNode(payload=2)
        tip3 = BigraphNode(payload=3)
        branch.insert_node(node=tip2, tip=False)
        branch.insert_node(node=tip3, tip=False)
        print(f"tip1: {str(tip1)}")
        print(f"tip2: {str(tip2)}")
        print(f"tip3: {str(tip3)}")
        # Branch should now look like (from beginning to tip): tip2->tip3->tip1
        self.assertEqual(tip1, branch.tip_node)
        self.assertEqual(None, branch.tip_node.successor)
        self.assertEqual(tip3, branch.tip_node.predecessor)
        self.assertEqual(tip1, tip3.successor)
        self.assertEqual(tip2, tip3.predecessor)
        self.assertEqual(tip3, tip2.successor)
        self.assertEqual(None, tip2.predecessor)


class Test_Bigraph(unittest.TestCase):
    def test_init_property_getters(self):
        node = BigraphNode(payload=1)
        graph = Bigraph(root=node)
        self.assertEqual(node, graph.root)

    def test_add_branch_len_getitem(self):
        graph = Bigraph()
        branch1 = Branch()
        branch2 = Branch()
        graph.add_branch(branch1)
        graph.add_branch(branch1) # Should do nothing. Can't add same branch twice.
        graph.add_branch(branch2)
        self.assertEqual(2, len(graph))
        self.assertEqual(branch1, graph[0])
        self.assertEqual(branch2, graph[1])





if __name__ == '__main__':
    unittest.main()
