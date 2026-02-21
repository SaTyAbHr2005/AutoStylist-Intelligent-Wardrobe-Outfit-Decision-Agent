from app.config.db import users_collection
from passlib.context import CryptContext

def set_password(email, password):
    pwd = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
    hashed = pwd.hash(password)
    result = users_collection.update_one({"email": email}, {"$set": {"hashed_password": hashed}})
    print('matched:', result.matched_count, 'modified:', result.modified_count)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: set_user_password.py email password')
    else:
        set_password(sys.argv[1], sys.argv[2])
