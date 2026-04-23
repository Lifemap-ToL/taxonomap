# taxonomap

Python package to interact with the [LifeMap](https://lifemap.univ-lyon1.fr/) taxonomy database.  
It allows you to convert between taxids and scientific names, and to explore the tree of life (ancestors, descendants, children, siblings, MRCA...).

---

## Installation

A discuter (rendre dispo sur PyPiI??). En attendant:

### Install from GitHub

---

```bash
git clone https://github.com/Lifemap-ToL/taxonomap.git
cd taxonomap
uv pip install .
```

### For development

```bash
git clone https://github.com/Lifemap-ToL/taxonomap.git
cd taxonomap
uv pip install -e .
```

---

## Functions

### `Conversions`

| Function | Description |
|---|---|
| `taxid_to_latin_name(taxid)` | Convert one or a list of NCBI taxids to scientific names |
| `latin_name_to_taxid(sci_name)` | Convert one or a list of scientific names to NCBI taxids (exact match) |
| `get_version()` | Fetch the last update date of the LifeMap database |

### `Phylogeny`

All phylogeny functions accept either a taxid (`int` or `str`) or a scientific name (`str`).

| Function | Description |
|---|---|
| `get_ascendant(value)` | Get the full lineage (list of ancestor taxids) of a taxon |
| `get_descendants(value)` | Get all descendant taxids of a taxon |
| `get_tips(value)` | Get all terminal (leaf) taxids of a taxon |
| `get_children(value)` | Get the direct children taxids of a taxon |
| `get_siblings(value)` | Get the sibling taxids of a taxon |
| `get_MRCA(*taxids)` | Find the Most Recent Common Ancestor of two or more taxids |


---

## Usage examples

### Example 1 — Convert names and explore lineage

```python
from taxonomap.conversions import taxid_to_latin_name, latin_name_to_taxid
from taxonomap.phylogeny import get_ascendant, get_children

# Convert taxid to scientific name
print(taxid_to_latin_name(9606))          # ['Homo sapiens']
print(taxid_to_latin_name([9606, 9685]))  # ['Homo sapiens', 'Felis catus']

# Convert scientific name to taxid
print(latin_name_to_taxid("Homo sapiens"))  # [9606]

# Get the full lineage of a taxon
lineage = get_ascendant(9606)
print(lineage)  # [9605, 207598, 9604, ...]

# Get the direct children of a taxon (works with name too)
children = get_children("Felis")
print(children)  # [9683, 9685, ...]
```

### Example 2 — Find the common ancestor of two species

```python
from taxonomap.phylogeny import get_MRCA

mrca = get_MRCA([9606, 9685])  # Human and cat
print(mrca) # {'taxid': 1437010, 'name': 'Boreoeutheria'}
print(mrca['taxid'])  # 1437010
print(mrca['name'])   # Boreoeutheria
```


---

## Developer documentation

### Building the documentation

The taxonomap project uses [Sphinx](https://www.sphinx-doc.org/) to generate an HTML documentation from the docstrings written inside the code.

Before starting:
```bash
# the documentation dependencies are already written in pyproject.toml
uv sync
```

How to build the documentationn:
```bash
cd docs
uv run make html
```

View the documentation:

The generated HTML files are located in `docs/_build/html/`.

Now open `docs/_build/html/index.html` in your browser to view the documentation :
```bash
# on Linux or macOS
open docs/_build/html/index.html

# on Windows
start docs/_build/html/index.html
```

Clean the build files:
```bash
cd docs
uv run make clean
```

NB: the `_build/` directory is git-ignored, and it should not be committed.