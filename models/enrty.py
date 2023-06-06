class Entry:
    def __init__(self, service, username, url, note, email, password):
        self.service = service
        self.username = username
        self.note = note
        self.url = url
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"""(
                service: {self.service}
                username: {self.username}
                note: {self.note}
                url: {self.url}
                email: {self.email}
                password: {self.password}
                )"""
