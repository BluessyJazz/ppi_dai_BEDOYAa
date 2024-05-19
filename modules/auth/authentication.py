"""
Este módulo ejecuta la lógica para el inicio de sesión, cierre de sesión,
registro de usuario, restablecimiento de contraseña, olvido de contraseña,
olvido de nombre de usuario y modificación de detalles de usuario.
"""

from typing import Optional
import streamlit as st

from ..utilities.hasher import Hasher
from ..utilities.validator import Validator
from ..utilities.helper import Helper
from ..utilities.exceptions import (CredentialsError,
                                    ForgotError,
                                    ResetError,
                                    UpdateError)


class AuthenticationHandler:
    """
    Esta clase ejecuta la lógica para el inicio de sesión, cierre de sesión,
    registro de usuario, restablecimiento de contraseña, olvido de contraseña,
    olvido de nombre de usuario y modificación de detalles de usuario.
    """
    def __init__(self, credentials: dict,
                 validator: Optional[Validator] = None):
        """
        Inicializa la clase AuthenticationHandler con las credenciales de los
        usuarios y el validador de entradas.

        Args:
            credentials (dict): Diccionario de credenciales de los usuarios.
            validator (Validator, opcional): Instancia de la clase Validator.
                Por defecto es None.

        Returns:
            None
        """

        self.credentials = credentials

        self.credentials['usernames'] = {
                                         key.lower(): value
                                         for key, value in credentials[
                                                                    'usernames'
                                                                      ].items()
                                        }

        if validator is not None:
            self.validator = validator
        else:
            self.validator = Validator()

        self.random_password = None

        for username, _ in self.credentials['usernames'].items():
            if 'logged_in' not in self.credentials['usernames'][username]:

                self.credentials['usernames'][username]['logged_in'] = False

            if not Hasher._is_hash(
                    self.credentials['usernames'][username]['password']):

                self.credentials['usernames'][username]['password'] = \
                    Hasher._hash(
                        self.credentials['usernames'][username]['password'])

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
        if 'user_id' not in st.session_state:
            st.session_state['user_id'] = None

    def check_credentials(self, identifier: str, password: str) -> bool:
        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        identifier: str
            The entered username or email.
        password: str
            The entered password.

        Returns
        -------
        bool
            Validity of the entered credentials.
        """

        for username, user_data in self.credentials['usernames'].items():
            if identifier == username or identifier == user_data['email']:
                try:
                    if Hasher.check_pw(password, self.credentials['usernames'][
                                        username]['password']):
                        return True
                    st.session_state['authentication_status'] = False
                    return False
                except TypeError as e:
                    print(e)
                except ValueError as e:
                    print(e)
        st.session_state['authentication_status'] = False
        return False

    def credentials_contains_value(self, value: str) -> bool:
        """
        Checks to see if a value is present in the credentials dictionary.

        Parameters
        ----------
        value: str
            Value being checked.

        Returns
        -------
        bool
            Presence/absence of the value, True: value present, False
            value absent.
        """
        found = False
        for d in self.credentials['usernames'].values():
            if value in d.values():
                found = True
                break
        return found

    def execute_login(self, username: Optional[str] = None,
                      token: Optional[dict] = None):
        """
        Executes login by setting authentication status to true and adding
        the user's
        username and name to the session state.

        Parameters
        ----------
        username: str
            The username of the user being logged in.
        token: dict
            The re-authentication cookie to retrieve the username from.
        """

        if username:
            # Obtener el nombre de usuario asociado al correo electrónico
            # username = self._get_username('email', identifier)

            # Si no se encontró un nombre de usuario, asumir que el
            # identificador es un nombre de usuario
            # if not username:
            #    username = identifier

            st.session_state['username'] = username
            name = self.credentials['usernames'][username]['name']
            st.session_state['name'] = name
            st.session_state['authentication_status'] = True
            self.credentials['usernames'][username]['logged_in'] = True
            user_id = self.credentials['usernames'][username]['id']
            st.session_state['user_id'] = user_id

        if token:
            st.session_state['username'] = token['username']
            name = self.credentials['usernames'][token['username']]['name']
            st.session_state['name'] = name
            st.session_state['authentication_status'] = True
            username = token['username']
            self.credentials['usernames'][username]['logged_in'] = True
            user_id = self.credentials['usernames'][username]['id']
            st.session_state['user_id'] = user_id

    def execute_logout(self):
        """
        Clears cookie and session state variables associated with the logged
        in user.
        """
        username = st.session_state['username']
        self.credentials['usernames'][username]['logged_in'] = False
        st.session_state['logout'] = True
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.session_state['authentication_status'] = None
        st.session_state['user_id'] = None

        return username

    def forgot_password(self, username: str) -> tuple:
        """
        Creates a new random password for the user.

        Parameters
        ----------
        username: str
            Username associated with the forgotten password.

        Returns
        -------
        tuple
            Username of the user; email of the user; new random password of
            the user.
        """
        if not self.validator.validate_length(username, 1):
            raise ForgotError('Username not provided')
        if username in self.credentials['usernames']:
            return (username, self.credentials['usernames'][username]['email'],
                    self._set_random_password(username))
        else:
            return False, None, None

    def forgot_username(self, email: str) -> tuple:
        """
        Retrieves the forgotten username of a user.

        Parameters
        ----------
        email: str
            Email associated with the forgotten username.

        Returns
        -------
        tuple
            Username of the user; email of the user.
        """
        if not self.validator.validate_length(email, 1):
            raise ForgotError('Email not provided')
        return self._get_username('email', email), email

    def get_user_details(self, username: str) -> tuple:
        """
        Retrieves the user's name and email.

        Parameters
        ----------
        username: str
            Username of the user.

        Returns
        -------
        tuple
            Name of the user; email of the user.
        """
        return self.credentials['usernames'][username]['name'], \
            self.credentials['usernames'][username]['email']

    def _get_username(self, key: str, value: str) -> str:
        """
        Retrieves the username based on a provided entry.

        Parameters
        ----------
        key: str
            Name of the credential to query i.e. "email".
        value: str
            Value of the queried credential i.e. "jsmith@gmail.com".

        Returns
        -------
        str
            Username associated with the given key, value pair i.e. "jsmith".
        """
        for username, values in self.credentials['usernames'].items():
            if values[key] == value:
                return username
        return False

    def _register_credentials(self, username: str, name: str, password: str,
                              email: str):
        """
        Adds the new user's information to the credentials dictionary.

        Parameters
        ----------
        username: str
            Username of the new user.
        name: str
            Name of the new user.
        password: str
            Password of the new user.
        email: str
            Email of the new user.
        pre-authorization: bool
            Pre-authorization requirement, True: user must be pre-authorized
            to register,
            False: any user can register.
        domains: list
            Required list of domains a new email must belong to i.e.
            ['gmail.com', 'yahoo.com'],
            list: the required list of domains, None: any domain is allowed.
        """

        hashed_pw = Hasher([password]).generate()[0]

        self.credentials['usernames'][username] = \
            {'email': email, 'logged_in': False,
             'name': name, 'password': hashed_pw}

        return name, email, username, hashed_pw

    def register_user(self, new_password: str,
                      new_username: str, new_name: str,
                      new_email: str) -> tuple:
        """
        Validates a new user's username, password, and email. Subsequently adds
        the validated user
        details to the credentials dictionary.

        Parameters
        ----------
        new_password: str
            Password of the new user.
        new_password_repeat: str
            Repeated password of the new user.
        pre-authorization: bool
            Pre-authorization requirement, True: user must be pre-authorized
            to register,
            False: any user can register.
        new_username: str
            Username of the new user.
        new_name: str
            Name of the new user.
        new_email: str
            Email of the new user.
        domains: list
            Required list of domains a new email must belong to i.e.
            ['gmail.com', 'yahoo.com'],
            list: the required list of domains, None: any domain is allowed.

        Returns
        -------
        tuple
            Email of the new user; username of the new user; name of the new
            user.
        """

        name = new_name
        username = new_username
        email = new_email
        password = new_password

        registered_credentials = self._register_credentials(username,
                                                            name,
                                                            password,
                                                            email)
        return registered_credentials

    def reset_password(self, username: str, password: str, new_password: str,
                       new_password_repeat: str) -> bool:
        """
        Validates the user's current password and subsequently saves their new
        password to the
        credentials dictionary.

        Parameters
        ----------
        username: str
            Username of the user.
        password: str
            Current password of the user.
        new_password: str
            New password of the user.
        new_password_repeat: str
            Repeated new password of the user.

        Returns
        -------
        bool
            State of resetting the password, True: password reset successfully.
        """
        if self.check_credentials(username, password):

            check_pw = self.validator.validate_password_strength(new_password)

            if check_pw != 'ok':
                raise ResetError(check_pw)

            if new_password != new_password_repeat:
                raise ResetError('Las contraseñas no coinciden')

            if password != new_password:
                self._update_password(username, new_password)
                return True
            else:
                raise ResetError('La nueva contraseña no puede ser igual \
                                  a la anterior')
        else:
            raise CredentialsError('password')

    def _set_random_password(self, username: str) -> str:
        """
        Updates the credentials dictionary with the user's hashed random
        password.

        Parameters
        ----------
        username: str
            Username of the user to set the random password for.

        Returns
        -------
        str
            New plain text password that should be transferred to the user
            securely.
        """
        self.random_password = Helper.generate_random_pw()
        self.credentials['usernames'][username]['password'] = \
            Hasher([self.random_password]).generate()[0]
        return self.random_password

    def _update_entry(self, username: str, key: str, value: str):
        """
        Updates the credentials dictionary with the user's updated entry.

        Parameters
        ----------
        username: str
            Username of the user to update the entry for.
        key: str
            Updated entry key i.e. "email".
        value: str
            Updated entry value i.e. "jsmith@gmail.com".
        """
        self.credentials['usernames'][username][key] = value

    def _update_password(self, username: str, password: str):
        """
        Updates the credentials dictionary with the user's hashed reset
        password.

        Parameters
        ----------
        username: str
            Username of the user to update the password for.
        password: str
            Updated plain text password.
        """
        self.credentials['usernames'][username]['password'] = \
            Hasher([password]).generate()[0]

    def update_user_details(self, new_value: str, username: str,
                            field: str) -> bool:
        """
        Validates the user's updated name or email and subsequently modifies
        it in the
        credentials dictionary.

        Parameters
        ----------
        new_value: str
            New value for the name or email.
        username: str
            Username of the user.
        field: str
            Field to update i.e. name or email.

        Returns
        -------
        bool
            State of updating the user's detail, True: details updated
            successfully.
        """
        if field == 'name':
            if not self.validator.validate_name(new_value):
                raise UpdateError('Name is not valid')
        if field == 'email':
            if not self.validator.validate_email(new_value):
                raise UpdateError('Email is not valid')
            if self.credentials_contains_value(new_value):
                raise UpdateError('Email already taken')
        if new_value != self.credentials['usernames'][username][field]:
            self._update_entry(username, field, new_value)
            if field == 'name':
                st.session_state['name'] = new_value
            return True
        else:
            raise UpdateError('New and current values are the same')

    def delete_user(self, username: str):
        """
        Deletes the user from the credentials dictionary.

        Parameters
        ----------
        username: str
            Username of the user to delete.
        """
        del self.credentials['usernames'][username]
