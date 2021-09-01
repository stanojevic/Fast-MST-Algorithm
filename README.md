# Fast MST Algorithm
Implementation of fast algorithms for (Maximum Spanning Tree) MST parsing that includes fast ArcMax+Reweighting+Tarjan algorithm for single-root dependency parsing.

## Usage
The implementation finds *Maximum* Spanning Tree. If you want minimum spanning tree instead you can provide negative weights. The implementation contains three components:
- Tarjan's algorithm for finding unconstrained MST
- Reweighting meta-algorithm for constraining MST to have only one ROOT edge (see reference below)
- ArcMax optimization for speed improvements on <em>easy</em> inputs

Everything relevant for MST dependency parsing can be accessed trough `fast_parse` function as shown here:

```
>>> from mst import fast_parse
>>> import numpy as np
>>> example_weights = np.random.rand(10, 10)
>>> fast_parse(example_weights, one_root=True)
array([-1, 8, 4, 6, 9, 8, 7, 2, 0, 1])
```

Input weight matrix weight `[i, j]` is interpreted the weight of arc going from j to i (j is the head while i is the dependent). Token 0 is treated at the root note of the MST (it doesn't have an incoming arc).

## References

The algorithms and their performance are presented in:

A Root of a Problem: Optimizing Single-Root Dependency Parsing<br/>
Miloš Stanojević and Shay B. Cohen<br/>
EMNLP 2021

