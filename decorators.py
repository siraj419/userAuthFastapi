def decorator(func):
    def wrapper(name):
        print("Before function")
        output = func(name)
        print("Output of function:", output)
        print("After function")
    return wrapper

@decorator
def say_hello(name):
    return "hello " + name

# decorated_func = decorator(say_hello)
# decorated_func()

say_hello("Ali")