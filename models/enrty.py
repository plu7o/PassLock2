class Entry:
    def __init__(self, service, username, url, email, password, id=None):
        self.id = id
        self.service = service
        self.username = username
        self.url = url
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"""(
                id: {self.id}
                service: {self.service}
                username: {self.username}
                url: {self.url}
                email: {self.email}
                password: {self.password}
                )"""
