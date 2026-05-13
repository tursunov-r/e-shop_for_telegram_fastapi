class MyRange:
    def __init__(self, *args):
        if len(args) == 1:
            self.start = 0
            self.end = args[0]
            self.step = 1
        elif len(args) == 2:
            self.start = args[0]
            self.end = args[1]
            self.step = 1
        elif len(args) == 3:
            self.start = args[0]
            self.end = args[1]
            self.step = args[2]
        else:
            raise ValueError(f"Wait 1-3 arguments, was take {len(args)}")
        self.current = self.start - self.step

    def __next__(self):
        self.current += self.step
        if (self.current >= self.end and self.step > 0) or (
            self.current <= self.end and self.step < 0
        ):
            raise StopIteration
        return self.current

    def __iter__(self):
        return self


for i in MyRange():
    print(i)
