
from example_module.ExampleClass import ExampleClass

e = ExampleClass()
print(e.example_method())

class AnotherClass:
    def __init__(self):
        print("AnotherClass instantiated")

    def another_method(self):
        return "Hello, another!"