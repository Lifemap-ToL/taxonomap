# taxonomap

Python package to interact with the [LifeMap](https://lifemap.univ-lyon1.fr/) taxonomy database.  
It allows you to convert between taxids and scientific names, and to explore the tree of life (ancestors, descendants, children, siblings, MRCA...).

---

## Installation

```bash
Avoir faut en discuter 

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

mrca = get_MRCA(9606, 9685)  # Human and cat
print(mrca['taxid'])  # taxid of the MRCA
print(mrca['name'])   # ['Boreoeutheria']
```
