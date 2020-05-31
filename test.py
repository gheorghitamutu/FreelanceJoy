class a:

    def __init__(self, name):
        self.name = name

obj = a("hello")

setattr(obj, "nam", "pisici")
print(obj.name)