import sqlite3
import sys
from string import ascii_letters, digits, punctuation
from random import choices, randint, sample

# maximum number of times to attempt replacing a character
MAX_TRIES = 1000

def create_password(
        length: int, 
        characters: str | None = None, 
        required=None, 
        n_required: int | None = None, 
        site: str | None = None,
        username: str | None = None,
) -> str:
    if characters is None:
        characters = ascii_letters + digits + punctuation

    if required is None:
        required = punctuation

    if n_required is None:
        n_required = 1

    password = choices(characters, k=length)

    # replace characters with required characters if necessary 
    if required is not None:
        password = _replace_characters_with_required(password, required, n_required)

    password = "".join(password)

    if site is not None and username is not None:
        # write to database
        # TODO: create a folder on the OS to put the db in
        connection = sqlite3.connect("password.db")
        cursor = connection.cursor()
        
        # TODO: encrypt password before writing to database

        if not _table_exists(cursor, "password"):
            _create_password_table(cursor)
        
        try:
            _insert_password(cursor, site, username, password)
            connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error: A password already exists for user '{username}' on '{site}'.")
            sys.exit(1)
        except Exception as e:
            connection.rollback()
            raise e
    elif (site is None and username is not None) or (site is not None and username is None):
        raise ValueError("site and username parameters must both be specified to save a password")

    return password


def _replace_characters_with_required(password: list[str], required: str, n_required: int) -> list[str]:
    # ensure the correct number of required characters are used
    required = "".join(sample(required, k=n_required))

    replaced = set()
    indexes = set()
    for c in required:
        if c not in replaced:
            index = randint(0, length - 1)
            tries = 0
            # get an index that has not been used yet
            while index in indexes and tries < MAX_TRIES:
                index = randint(0, length - 1)
                tries += 1
            if tries >= MAX_TRIES:
                # could not replace the current character
                raise ValueError("Could not create a password with the requested length and required characters. Check that the requested length is greater than the number of required characters.")
            indexes.add(index)
            password[index] = c
            replaced.add(c)
    return password

def _table_exists(cursor, table: str) -> bool:
    res = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (table, ));
    return bool(res.fetchone()[0])

def _create_password_table(cursor):
    cursor.execute("""
        CREATE TABLE password(
            site, 
            username,
            password,
            PRIMARY KEY (site, username)
        );
        """)

def _insert_password(cursor, site, username, password):
    cursor.execute("INSERT INTO password VALUES (?, ?, ?);", (site, username, password))

def _parse_arg(i, arg, short_name, long_name, parser=None):
    if parser is None:
        parser = lambda x: x
    if arg in (short_name, long_name):
        return parser(sys.argv[i+1])
    elif arg.startswith(f"{long_name}="):
        return parser(arg.replace(f"{long_name}=", ""))

    return None

if __name__ == "__main__":
    length = int(sys.argv[1])
    characters = None
    required = None
    n_required = None
    site = None
    username = None
    for i, arg in enumerate(sys.argv):
        if (characters_parsed := _parse_arg(i, arg, "-c", "--characters")) is not None:
            characters = characters_parsed
        if (required_parsed := _parse_arg(i, arg, "-r", "--required")) is not None:
            required = required_parsed
        if (n_required_parsed := _parse_arg(i, arg, "-n", "--n-required")) is not None:
            n_required = n_required_parsed
        if (site_parsed := _parse_arg(i, arg, "-s", "--site")) is not None:
            site = site_parsed
        if (username_parsed := _parse_arg(i, arg, "-u", "--username")) is not None:
            username = username_parsed
    print(
        create_password(
            length, 
            characters=characters, 
            required=required, 
            n_required=n_required,
            site=site,
            username=username,
        )
    )

                
                
                
