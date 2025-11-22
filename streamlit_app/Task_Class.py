from Car_Class import Car
import global_vars

class Task:

    def __init__(self, address, message_short, message_text):
        self._address = address
        self._msg_short = message_short
        self._msg_text = message_text

        # private
        self._cars = []       # list of the cars in this call
        self._infos = []      # list with the infos


    # adder
    def add_car(self, car_name):
        car = Car(car_name)
        self._cars.append(car)

    def set_next_status(self, car_name):
        car = self.get_car(car_name)
        car.set_next_status()
        return self._hasTaskEnded()
    
    def _hasTaskEnded(self):
        if not(global_vars.auto_delete):
            return False

        for car in self._cars:
            if car.get_status() != 1:
                return False
        
        return True


    def add_info(self, info):
        self._infos.append(info)

    # deletes
    def delete_last_car(self):
        self._cars.pop()

    def delete_last_info(self):
        self._infos.pop()

    # getter
    def get_address(self):
        return self._address
    
    def get_message_short(self):
        return self._msg_short

    def get_message_text(self):
        return self._msg_text
    
    def get_cars(self):
        return self._cars
    
    def get_cars_name(self):
        cars = []
        for car in self._cars:
            cars.append(car.get_name())
        return cars
    
    def get_car(self, car_name):
        for car in self._cars:
           if car.get_name() == car_name:
               return car
    
    def get_cars_status(self):
        cars = []
        for car in self._cars:
            cars.append(str(car.get_status()))
        return cars
    
    def get_cars_with_status(self):
        cars = []
        for car in self._cars:
            cars.append((car.get_name(), car.get_status()))
        return cars

    def get_infos(self):
        return self._infos
        


    
