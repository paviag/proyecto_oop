import argon2
import file_handling as file

_hasher = argon2.PasswordHasher(time_cost=3, memory_cost=64*1024, salt_len=16,
                               parallelism=1, hash_len=32, encoding='utf-8')

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

def change_account_info(*, current_password: str, new_password: str = None,
                        new_user: str = None) -> None:
    """Modifies account information if the given current password is valid.
        
    Parameters:
    current_password (str): Currently stored password.
    new_password (str): New password to store.
    new_user (str): New user to store.
    """
    # Checks if current password given is correct
    if current_password != None:
        if verify_password(current_password):
            if not(new_user==None and new_password==None):
                if new_user != None:
                    # Checks if new user abides by rules, modifies it if so and raises exception if not
                    if new_user.strip()!="" and new_user.isascii() and new_user.isalnum():
                        file.write_over_file('admin.txt', 'Usuario', new_user)
                    else:
                        raise Exception('El usuario no puede contener tildes, espacios o demás caracteres especiales.')
                if new_password != None:
                    # Checks if new user abides by rules, modifies it if so and raises exception if not
                    if new_password.strip()!="" and new_password.isascii() and new_password.isalnum():
                        # Modifies stored password hash
                        new_password_hash = _hasher.hash(new_password)
                        file.write_over_file('admin.txt', 'Clave', new_password_hash)
                    else:
                        raise Exception('La contraseña no puede contener tildes, espacios o demás caracteres especiales.')
            else:
                raise Exception('No se ingresó ningún campo a cambiar.')
        else:
            raise Exception('La contraseña ingresada es incorrecta.')
    else:
        raise Exception('No se ingresó contraseña actual.')