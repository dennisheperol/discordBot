class ScavengeTime:
    def __init__(self, object_info):
        self.id = object_info[0]
        self.time = object_info[1]

    def get_id(self):
        return self.id

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time
