class Quad:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.type = self.get_type()
        self.s = self.get_s()
        self.p = self.get_p()

    def __str__(self):
        return f"{self.type}, Длина: {self.a}, Ширина: {self.b}, Площадь: {self.s}, Периметр: {self.p}"

    def get_s(self):
        return (self.a+self.b)*2

    def get_p(self):
        return self.a * self.b

    def get_type(self):
        if self.a == self.b:
            return "Квадрат"
        else:
            return "Параллелограмм"

rectangle = Quad(3, 8)
square = Quad(5, 5)

print(rectangle)
print(square)