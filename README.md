# Password Manager

A little utility script for generating and managing passwords offline.

## Usage

### Randomly generating passwords

If you are not in the directory containing `password.py`, replace `password.py` with a path to the script.

```bash
# create a password with length 16
python password.py 16


# create a password for a specific site and username and save it
python password.py 16 --username test_user --site example.com
```


It is useful to define the following function in your bashrc or zshrc for quicker usage:

```bash
function password {
    python password.py $@
}
```

## TODOs:
- Add help command
- Add commands to retrieve passwords for a site and username or all passwords for a username
- Encrypt passwords when writing to the db and decrypt when reading
