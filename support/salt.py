import bcrypt
import sys

def hash_password(password: str):
    # bcrypt automatically generates the salt when hashing the password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python salt.py <password>")
        sys.exit(1)

    password = sys.argv[1]
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
