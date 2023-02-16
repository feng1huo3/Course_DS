from abc import ABC
from engine import Engine


class Error(Exception):
    """Класс исключений, кроме указанных"""
    pass


class LowFuelError(Exception):
    """Вызывается, когда топлива в баке нет"""
    pass


class NotEnoughFuel(Exception):
    """Вызывается, когда топлива недостаточно для перемещения
    на заданную дистанцию"""
    pass


class CargoOverLoad(Exception):
    """Сообщает о перегрузе"""
    pass


class Vehicle(ABC):

    def __init__(self, weight=0, started=False, fuel=0, fuel_consumption=0):
        self.weight = weight
        self.started = started
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if not self.started:
            if self.fuel > 0:
                self.started = True  # обновляет состояние стартед
            else:
                raise LowFuelError

    def move(self, distance):
        full = self.fuel * 100 / self.fuel_consumption
        if full >= distance:
            print('Греби, давай!')
        else:
            raise NotEnoughFuel


class Car(Vehicle):
    def __init__(self, weight, started, fuel, fuel_consumption, engine):
        super().__init__(weight, started, fuel, fuel_consumption)
        self.engine = engine

    def set_engine(self, engine):
        self.engine = engine


class Plane(Vehicle):
    def __init__(self, weight, started, fuel, fuel_consumption, cargo, max_cargo):
        super().__init__(weight, started, fuel, fuel_consumption)
        self.cargo = cargo
        self.max_cargo = max_cargo

    def load_cargo(self, load):
        if self.cargo + load <= self.max_cargo:
            self.cargo += load
        else:
            raise CargoOverLoad

    def remove_all_cargo(self):
        temp = self.cargo
        self.cargo = 0
        return temp


class VehicleInitError(Exception):
    pass


def main():  # Проверим, что классы работают так, как задумано
    try:
        vehicles = []
        vehicles.append(Car(2000, True, 50, 10, Engine(1.6, 4)))
        vehicles.append(Car(7000, False, 500, 25, Engine(14.9, 8)))
        vehicles.append(Plane(45000, True, 10000, 400, 200, 500))
        # vehicles.append(Car(50, False, 0, 0, 0))
    except Exception as e:
        raise VehicleInitError(e)

    # client
    for vehicle in vehicles:
        vehicle.start()
        vehicle.move(100)

    vehicles[2].load_cargo(200)

    print(vehicles[2].cargo)
    print(vehicles[2].remove_all_cargo())
    print(vehicles[2].cargo)


try:
    main()
except LowFuelError as e:
    print(f'заправься! {e}')
    exit(4)
except NotEnoughFuel as e:
    print(f'Маловато будет! {e}')
    exit(3)
except CargoOverLoad as e:
    print(f'Скромнее надо быть! {e}')
    exit(2)
except Exception as e:
    print(e)
    exit(1)
