class Player:
    def __init__(self, user_id, arrival_time, address, char):
        self.user_id = user_id
        self.arrival_time = arrival_time
        self.address = address
        self.status = "Available"
        self.char = char

    def get_user_id(self):
        return self.user_id

    def get_arrival_time(self):
        return self.arrival_time

    def get_address(self):
        return self.address

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_char(self):
        return self.char

    def set_char(self, char):
        self.char = char
