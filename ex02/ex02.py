def multiply_all(*args: int)->int:
    result = 1
    for num in args:
        result *=num
    return result

print(multiply_all(2)) 