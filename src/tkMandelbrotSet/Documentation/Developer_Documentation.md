This file contains developer documentation for the tkMandelbrotSet package.

# Bi-directional graph for storing a tree of set zooms

## Working through required operations

Note that other operations on bigraphs may be useful in other contexts. The list below is focused on operations required for
using a bigraph as the data structure for storing zooming information for exploring a Mandelbrot set.

1. Must be able to add a node to the end of a branch. This is the typical "zoom in some more" operation. Implement in Branch class
   as add_node() method, to be assisted by insert_node() method in BigraphNode class. {done}
2. Must be able to "prune" a branch by moving the tip down to a selected node along a branch. This should remove all nodes "above"
   the selected node, even if there are multiple branches and thus tips beyond the selected node. If there are multiple branches,
   a question is, which branch name is retained for the new tip? This is the operation of backing up to a particular node and starting
   over zooming from there. Implement in Bigraph class as prune(from_node=?) method.
3. Must be able to "split" a node to start a new branch. This is the operation of backup to a particular node and beginning a new
   zooming exploration from there. Implement in Bigraph class as add_branch(at_node=split_point) method. {done}
4. Must be able to move "forward" toward the tip node of a branch. What happens when a branch split is encountered? Implemented in
   in BigraphNode class as successor property getter. {done}
1. Must be able to move backwards toward the root node. Implemented in BigraphNode class as predecessor property getter. {done}
