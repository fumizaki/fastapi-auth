import hashlib
import secrets


# https://kinsta.com/jp/blog/python-hashing/


def _generate_salt() -> str:
    return secrets.token_hex(16)


def _generate_stretching() -> int:
    return 10


def _hash_sha256(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()


class HashClient:
    
    def salt() -> str:
        return _generate_salt()
    
    def stretching() -> int:
        return _generate_stretching()
    
    def hash(password: str, salt: str, stretching: int) -> str:
        if stretching < 1:
            raise ValueError('stretching must be greater than or equal to 1')
        
        for _ in range(stretching):
            password = _hash_sha256(password, salt)
            
        return password
    
    def verify(password: str, salt: str, stretching: int, hashed: str) -> bool:
        return HashClient.hash(password, salt, stretching) == hashed