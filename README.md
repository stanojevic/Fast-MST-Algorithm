# Fast MST Algorithm
Implementation of the fast algorithm for Single-Root Maximum Spanning Tree by [Stanojević and Cohen (EMNLP 2021)](#references).

## Installation

```bash
pip install git+https://github.com/stanojevic/Fast-MST-Algorithm
```

## Usage
The implementation finds *Maximum* Spanning Tree. If you want minimum spanning tree instead you can provide negative weights. The implementation contains three components:
- Tarjan's algorithm for finding unconstrained MST
- Reweighting meta-algorithm for constraining MST to have only one ROOT edge (see reference below)
- ArcMax optimization for speed improvements on <em>easy</em> inputs

Everything relevant for MST dependency parsing can be accessed trough `fast_parse` function as shown here:

```python
>>> from mst import fast_parse
>>> import numpy as np
>>> np.random.seed(42)
>>> example_weights = np.random.rand(10, 10)
>>> fast_parse(example_weights, one_root=True)
array([-1,  0,  1,  5,  3,  2,  8,  6,  3,  6])
>>> fast_parse(example_weights, one_root=False)
array([-1,  0,  5,  7,  3,  3,  7,  0,  3,  6])
```

Input matrix weight `[i, j]` is interpreted the weight of arc going from i to j (i is the head while j is the dependent). Token 0 is treated at the root note of the MST (it doesn't have an incoming arc).
Note that this order of head and dependent is different from the presentation in the paper.

## References

```latex
@inproceedings{stanojevic:cohen,
 title = {A Root of a Problem: Optimizing Single-Root Dependency Parsing},
 author = {Stanojevi\'{c}, Milo\v{s} and Cohen, Shay B.},
 booktitle = {Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing},
 month = {November},
 year = {2021},
 publisher = {Association for Computational Linguistics},
 url = {https://stanojevic.github.io/papers/EMNLP_2021_Single_Root.pdf},
}
```
