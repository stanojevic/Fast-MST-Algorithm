# Fast MST Algorithm
Implementation of the fast algorithm for Single-Root Maximum Spanning Tree by [Stanojević and Cohen (EMNLP 2021)](https://aclanthology.org/2021.emnlp-main.823.pdf).

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

>>> W = np.random.rand(5, 5)

>>> fast_parse(W, one_root=False)
array([-1,  2,  0,  4,  0])

>>> fast_parse(W, one_root=True)
array([-1,  2,  0,  4,  2])
```

Input matrix weight `[i, j]` is interpreted the weight of arc going from i to j (i is the head while j is the dependent). Token 0 is treated at the root note of the MST (it doesn't have an incoming arc).
Note that this order of head and dependent is different from the presentation in the paper.

## References

```
@inproceedings{stanojevic-cohen-2021-root,
    title = "A Root of a Problem: Optimizing Single-Root Dependency Parsing",
    author = "Stanojevi{\'c}, Milo{\v{s}}  and Cohen, Shay B.",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.823",
    pages = "10540--10557",
    abstract = "We describe two approaches to single-root dependency parsing that yield significant speed ups in such parsing. One approach has been previously used in dependency parsers in practice, but remains undocumented in the parsing literature, and is considered a heuristic. We show that this approach actually finds the optimal dependency tree. The second approach relies on simple reweighting of the inference graph being input to the dependency parser and has an optimal running time. Here, we again show that this approach is fully correct and identifies the highest-scoring parse tree. Our experiments demonstrate a manyfold speed up compared to a previous graph-based state-of-the-art parser without any loss in accuracy or optimality.",
}
```
