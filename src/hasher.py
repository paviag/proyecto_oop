import argon2
import file_handling as file

_hasher = argon2.PasswordHasher(time_cost=3, memory_cost=64*1024, salt_len=16,
                               parallelism=1, hash_len=32, encoding='utf-8')

def change_password(current_password: str, new_password: str) -> None:
    """Changes stored password if the given current password is valid.
        
    Parameters:
    current_password (str): Currently stored password.
    new_password (str): New password to store.
    """
    if _hasher.verify_password(current_password):
        new_password_hash = _hasher.hash(new_password)
        file.write_over_file('admin.txt', 'Clave', new_password_hash)
    else:
        raise Exception('La contraseña ingresada es incorrecta.')
            
def verify_password(string: str) -> bool:
    """Returns True if the string matches the stored password or False
    if not.
        
    Parameters:
    string (str): String to compare to stored password.
    """
    stored_password_hash = file.get_content_by_field('admin.txt', 'Clave')
    try:
        _hasher.verify(stored_password_hash, string)
        file.write_over_file('admin.txt', 'Clave', _hasher.hash(string))
        return True
    except:
        return False