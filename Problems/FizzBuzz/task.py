for n in range(1, 101):
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    if len(result) == 0:
        result = n
    print(result)
