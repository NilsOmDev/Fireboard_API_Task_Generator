class Car:

    _status_numbers = [2, 3, 4, 1]

    def __init__(self, car_name):
        self._car_name = car_name
        self._curr_status_idx = 0

    def set_next_status(self):
        self._curr_status_idx += 1
        if self._curr_status_idx >= len(self._status_numbers):
            self._curr_status_idx = 0

    def get_status(self):
        return self._status_numbers[self._curr_status_idx]
    
    def get_name(self):
        return self._car_name
