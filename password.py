import sys
from string import ascii_letters, digits, punctuation
from random import choices, randint, sample

# maximum number of times to attempt replacing a character
MAX_TRIES = 1000

def create_password(length, characters=None, required=None, n_required=1):
    if characters is None:
        characters = ascii_letters + digits + punctuation

    if required is None:
        required = punctuation

    if n_required is None:
        n_required = 1

    password = choices(characters, k=length)

    # replace characters with required characters if necessary 
    if required is not None:
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

    return "".join(password)

if __name__ == "__main__":
    length = int(sys.argv[1])
    characters = None
    required = None
    n_required = None
    for i, arg in enumerate(sys.argv):
        if arg in ("-c", "--characters"):
            characters = sys.argv[i+1]
        elif arg.startswith("--characters="):
            characters = arg.replace("--characters=", "")

        if arg in ("-r", "--required"):
            required = sys.argv[i+1]
        elif arg.startswith("--required="):
            required = arg.replace("--required=", "")

        if arg in ("-n", "--n-required"):
            n_required = int(sys.argv[i+1])
        elif arg.startswith("--n-required="):
            n_required = int(arg.replace("--n-required=", ""))

    print(
        create_password(
            length, 
            characters=characters, 
            required=required, 
            n_required=n_required
        )
    )

                
                
                
