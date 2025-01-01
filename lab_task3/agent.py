# agent.py
class Student:
    def __init__(self, id, availability, preferences):
        self.id = id
        self.availability = availability
        self.preferences = preferences
        self.schedule = []

    def can_attend(self, time_slot):
        return time_slot in self.availability

    def get_preference(self, time_slot):
        return self.preferences.get(time_slot, 0)

    def assign_class(self, class_time):
        self.schedule.append(class_time)

    def reset_schedule(self):
        self.schedule = []