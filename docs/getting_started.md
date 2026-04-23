# Getting Started

Welcome to **taxonomap**! This guide will help you to get started.


## Installation

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


## Quick Examples

### Convert taxids to scientific names

```python
from taxonomap.conversions import taxid_to_latin_name

# For a single taxid...
name = taxid_to_latin_name(9606)
print(name)
# >>> ['Homo sapiens']

# ... Or multiple taxids!
names = taxid_to_latin_name([9606, 9685, 965])
print(names)
# >>> ['Homo sapiens', 'Felis catus', 'Oceanospirillum']
```


