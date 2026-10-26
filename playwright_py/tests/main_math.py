INSTANT = 10
PERSISTANT = 20

print(INSTANT + PERSISTANT)

# =====================================================
# PYTHON: funkcje, metody, logika, pętle
# Uruchom: python3 main_math.py
# =====================================================


# ---------- 1. ZMIENNE I TYPY ----------
name = "Mateusz"      # str
age = 30              # int
price = 9.99          # float
active = True         # bool
nothing = None        # NoneType

print(type(name), type(age), type(price), type(active), type(nothing))
print(f"{name} ma {age} lat")   # f-string

# ---------- 2. OPERATORY ----------
a, b = 7, 2
print(a + b, a - b, a * b)
print(a / b)    # 3.5  dzielenie zwykłe
print(a // b)   # 3    dzielenie całkowite
print(a % b)    # 1    reszta
print(a ** b)   # 49   potęga

# ---------- 3. LOGIKA: if / elif / else ----------
def check_number(n):
    if n > 0:
        return "dodatnia"
    elif n < 0:
        return "ujemna"
    else:
        return "zero"

print(check_number(5), check_number(-3), check_number(0))

x = 15
print(x > 10 and x < 20)   # True
print(x < 10 or x == 15)   # True
print(not x == 15)         # False
print(3 in [1, 2, 3])      # True
print(x is None)           # False

label = "parzysta" if x % 2 == 0 else "nieparzysta"   # ternary
print(label)

# ---------- 4. FUNKCJE ----------
def add(a, b):
    return a + b

def power(base, exp=2):          # argument domyślny
    return base ** exp

def total(*numbers):             # *args -> krotka
    return sum(numbers)

def describe(**info):            # **kwargs -> słownik
    return info

print(add(2, 3))
print(power(4), power(2, 10))
print(power(exp=3, base=2))      # argumenty nazwane
print(total(1, 2, 3, 4))
print(describe(name="Ala", age=25))

square = lambda n: n * n         # lambda
print(square(6))

# ---------- 5. PĘTLE ----------
# Uwaga: "for e in INSTANT" nie działa, int nie jest iterowalny -> użyj range()
for e in range(INSTANT):
    print("hi", e)

for i in range(1, 10, 2):        # start, stop, krok
    print(i, end=" ")
print()

fruits = ["jablko", "banan", "wisnia"]
for idx, fruit in enumerate(fruits):
    print(idx, fruit)

count = 3
while count > 0:                 # while
    print("odliczanie", count)
    count -= 1

for n in range(10):              # break / continue
    if n == 3:
        continue                 # pomiń 3
    if n == 6:
        break                    # zakończ pętlę
    print(n, end=" ")
print()

# ---------- 6. LISTY (metody) ----------
nums = [5, 2, 8, 1]
nums.append(10)          # dodaj na koniec
nums.insert(0, 99)       # wstaw na pozycję
nums.remove(2)           # usuń wartość
last = nums.pop()        # usuń i zwróć ostatni
nums.sort()              # sortuj w miejscu
nums.reverse()
print(nums, last, len(nums), max(nums), min(nums), sum(nums))
print(nums[0], nums[-1], nums[1:3])   # indeks i slice

squares = [n ** 2 for n in range(6)]              # list comprehension
evens = [n for n in range(10) if n % 2 == 0]
print(squares, evens)

# ---------- 7. STRINGI (metody) ----------
text = "  Hello World  "
print(text.strip())
print(text.lower(), text.upper())
print(text.replace("World", "Python"))
print(text.strip().split(" "))
print("-".join(["a", "b", "c"]))
print("Hello".startswith("He"), "Hello".endswith("lo"))
print("Hello"[::-1])        # odwrócenie

# ---------- 8. SŁOWNIKI (metody) ----------
user = {"name": "Ala", "age": 25}
user["city"] = "Warszawa"
print(user.get("email", "brak"))     # bezpieczne pobranie
print(user.keys(), user.values())
for key, value in user.items():
    print(key, "->", value)
user.pop("age")
print("name" in user)

cubes = {n: n ** 3 for n in range(4)}   # dict comprehension
print(cubes)

# ---------- 9. KROTKI I ZBIORY ----------
point = (3, 4)                       # krotka, niezmienna
px, py = point                       # rozpakowanie
unique = set([1, 2, 2, 3, 3])        # zbiór bez duplikatów
print(px, py, unique)
print({1, 2, 3} & {2, 3, 4})         # część wspólna
print({1, 2} | {2, 3})               # suma

# ---------- 10. BŁĘDY ----------
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "nie dziel przez zero"
    finally:
        pass                         # wykona się zawsze

print(safe_divide(10, 2), safe_divide(1, 0))

# ---------- 11. KLASY I METODY ----------
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

calc = Calculator(2)
calc.add(3).multiply(4)
print(calc)                          # Calculator(20)


# ---------- 12. ZADANIA DO ROZWIĄZANIA ----------

# TODO 1: is_even(n) -> True gdy parzysta
def is_even(n):
    return n % 2 == 0

# TODO 2: factorial(n) pętlą for, factorial(5) == 120
def factorial(n):
    result = 1
    for i in range(1, n + 1):   # range(1, 6) daje 1,2,3,4,5
        result=result*i                  # tu pomnóż result przez i
    return result

# TODO 3: fizzbuzz(n): dla 1..n wypisz "Fizz" (/3), "Buzz" (/5),
#         "FizzBuzz" (/3 i /5), w innym wypadku liczbę
def fizzbuzz(n):
    pass

# TODO 4: is_prime(n) -> True gdy pierwsza
def is_prime(n):
    pass

# TODO 5: average(numbers) -> średnia z listy (pusta lista -> 0)
def average(numbers):
    pass

# TODO 6: fibonacci(n) -> lista pierwszych n liczb Fibonacciego
def fibonacci(n):
    pass

# TODO 7: count_words(text) -> słownik {słowo: ile razy}
def count_words(text):
    pass

# TODO 8: reverse_string(s) bez [::-1] (użyj pętli)
def reverse_string(s):
    pass


# ---------- TESTY (odkomentuj gdy rozwiążesz) ----------
# assert is_even(4) is True and is_even(7) is False
# assert factorial(5) == 120
# assert is_prime(7) and not is_prime(9)
# assert average([2, 4, 6]) == 4 and average([]) == 0
# assert fibonacci(6) == [0, 1, 1, 2, 3, 5]
# assert count_words("a b a") == {"a": 2, "b": 1}
# assert reverse_string("abc") == "cba"
# fizzbuzz(15)
# print("Wszystko OK!")