# ChronoFidelius

ChronoFidelius is a Python library for plaintext encryption using homophonic substitution and historical character frequencies. It provides configurable error injection, frequency-based key generation, and advanced encryption techniques inspired by historical cryptography.

---

## Features
- **Homophonic Substitution Cipher**: Encrypts plaintext with multiple cipher options for each character.
- **Frequency-Based Key Generation**: Supports even and uneven key generation using historical unigram frequencies.
- **Error Injection**: Introduces errors (additions, deletions, or doubles) into plaintext for obfuscation.
- **Custom Configurations**: Control error frequency, character spacing, and more.

---

## Installation

Install `ChronoFidelius` using `pip` (after publishing the package to PyPI):

```bash
pip install ChronoFidelius
```

Or, install directly from the source:

```bash
git clone https://github.com/mbruton0426/ChronoFidelius.git
cd ChronoFidelius
pip install .
```

---

## Usage

### Basic Example:
```python
from chronofidelius import ChronoFidelius

# Initialize the ChronoFidelius object
cf = ChronoFidelius(
    plaintext="Hello, World!",
    include_errors=True,
    error_type="all",
    set_seed=42
)

# Perform all encryption methods using included historical frequencies
cf.encrypt_homophonic()

# Access the generated ciphertext and encryption dictionary
print(cf.pt_ct_dict)
```
### Specific Encryption Method Example
To specify the type of encryption:
```python
cf.encrypt_homophonic(key_type="even")
```

### Custom Frequency-Based Encryption Example
You can also provide custom character frequencies

```python
# Custom frequency dictionary
custom_frequencies = {"A": 0.1, "B": 0.2, "C": 0.3, "D": 0.4}

# Perform uneven encryption
cf.encrypt_homophonic(key_type="uneven", set_frequencies=custom_frequencies)
```

---

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
