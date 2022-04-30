import matplotlib.pyplot as plt
from io import StringIO
import base64
import json


class Plotter:
    def __init__(self, point, element):
        self.point = point
        self.element = element
        self.period = eval(" ".join(self.element["T"].split()[:-1]))

    def get_dimensions(self):
        middle = self.get_middle()
        if middle:
            if middle - self.period >= 0:
                if middle - self.period * 2 >= 0:
                    return [middle - self.period * x for x in range(2, -3, -1)]
                return [middle - self.period * x for x in range(1, -4, -1)]
            return [middle + self.period * x for x in range(5)][::-1]
        return [self.period * x for x in range(5)]

    def get_middle(self):
        if self.point < 0:
            return 0
        
        bottom = abs(self.point // self.period * self.period - self.point)
        top = round(self.point / self.period) * self.period - \
            self.point if self.point >= self.period else self.period - self.point
        min_distance = min(bottom, top)
        if min_distance == bottom:
            return self.point - bottom
        return self.point + top

    def create_plot(self):
        plt.switch_backend('Agg')

        self.x = self.get_dimensions()
        self.y = [1 / (2 ** (point // self.period))
                  if point else 1 for point in self.x]

        fig, ax = plt.subplots()

        if self.point > self.period * len(self.y):
            plt.scatter(self.point, 0,
                    color='orange', s=40, marker='o')    
        else:
            plt.scatter(self.point, 1 / (2 ** (self.point / self.period)),
                    color='orange', s=40, marker='o')

        if self.element["dimension"] == "years":
            plt.xlabel("t, лет")
        if self.element["dimension"] == "minutes":
            plt.xlabel("t, минут")
        if self.element["dimension"] == "seconds":
            plt.xlabel("t, секунд")
        if self.element["dimension"] == "days":
            plt.xlabel("t, дней")
        if self.element["dimension"] == "hours":
            plt.xlabel("t, часов")
        plt.ylabel("Доля атомов, N₀")

        plt.ylim(self.y[0], self.y[-1])

        plt.plot(self.x, self.y)

        plt.savefig(self.element["symbol"] + str(self.point) + '.png')


class Element:
    def __init__(self, number):
        self.number = number
        
        for element in elements:
            if element["number"] == self.number:
                self.elem = element
                self.mass_number = element["mass number"]
                self.name = element["name"]
                self.symbol = element["symbol"]
                self.period = element["T"]
                self.radiation = element["radiation"]
                break

    def __repr__(self):
        return f"""Элемент {self.name} ({self.symbol}):
Порядковый номер: {self.number}
Массовое число изотопа: {self.mass_number}
Период полураспада: {self.period}
Излучение: {self.radiation}
"""

    def __call__(self):
        return self.elem


numbers = ['89', '95', '85', '7', '4', '97', '83', '83', '83', '1', '26', '77', '53', '19', '98', '48', '27', '96', '99', '100', '15', '87', '9', '9', '103', '101', '11', '11', '93', '102', '91', '61', '84', '84', '94', '94', '94', '94', '88', '86', '37', '37', '16', '43', '90', '92', '92', '92', '92', '92', '6', '55']
elements = json.load(open("elements.json", encoding="utf-8"))