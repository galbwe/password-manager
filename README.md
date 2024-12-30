# Password Manager

A little utility script for generating and managing passwords offline.

## Usage

### Randomly generating passwords

If you are not in the directory containing `password.py`, replace `password.py` with a path to the script.

```python
# create a password with length 16
python password.py 16
```

It is useful to define the following function in your bashrc or zshrc for quicker usage:

```bash
function password {
    python password.py $@
}
```

## TODOs:
- Add functionality to save passwords to a sqlite database.
- Compile code to a binary with cython so a python interpretter is not required to run the scripts.
