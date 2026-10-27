def is_even(n):
    return n % 2 == 0

class Calculator:
    def __init__(self, start=0):
        self.value = start

    def add(self, n):
        self.value += n
        return self                  # pozwala łańcuchować

    def multiply(self, n):
        self.value *= n
        return self

    def __str__(self):
        return f"Calculator({self.value})"

calc = Calculator(12)
calc.add(3).multiply(4)
print(calc) 


class Cat:
    def __init__(self, name, age=1):   # age ma wartość domyślną
        self.name = name
        self.age = age
        self.hungry = True

    def feed(self):
        self.hungry = False            # zmiana atrybutu

    def birthday(self):
        self.age += 1
        return self.age                # metoda może zwracać wartość

    def __str__(self):                 # co wypisze print(obiekt)
        status = "głodny" if self.hungry else "najedzony"
        return f"{self.name}, {self.age} lat, {status}"


kitty = Cat("Kitty", 3)
print(kitty)              # Kitty, 3 lat, głodny
kitty.feed()
kitty.birthday()
print(kitty)              # Kitty, 4 lat, najedzony


kitty = Cat("Kitty")     # tworzenie obiektu (instancji)
print(kitty.name) 

kitty = Cat("Kitty")
tom = Cat("Tom")
print(kitty.name, tom.name)   # Kitty Tom
