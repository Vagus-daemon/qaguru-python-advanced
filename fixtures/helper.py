import requests


class Helper:

    def __init__(self, host: str):
        self.host = host
        self.session = requests.Session()

    def get_app_status(self):
        return requests.get(f"{self.host}/status/")

    def get_all_users(self):
        return requests.get(f"{self.host}/api/users/")

    def get_one_user(self, user_id: int):
        return requests.get(f"{self.host}/api/users/{user_id}")

    def create_new_user(self, email: str, first_name: str, last_name: str, avatar: str):
        user_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "avatar": avatar,
        }
        return requests.post(f"{self.host}/api/users/", json=user_data)

    def delete_one_user(self, user_id: int):
        return requests.delete(f"{self.host}/api/users/{user_id}")

    def update_user_data(self, user_id: int, email: str = None, first_name: str = None, last_name: str = None,
                         avatar: str = None):
        user_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "avatar": avatar,
        }
        return requests.patch(f"{self.host}/api/users/{user_id}", json=user_data)
