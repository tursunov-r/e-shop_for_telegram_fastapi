nums = "1,2,3,5,10,11,22"
nums = list(map(int, nums.split(",")))

result = []
start = nums[0]
prev = nums[0]

for num in nums[1:]:
    if num == prev + 1:
        prev = num
    else:
        if start == prev:
            result.append(str(start))
        else:
            result.append(f"{start}-{prev}")
        start = num
        prev = num

if start == prev:
    result.append(str(start))
else:
    result.append(f"{start}-{prev}")

result = ",".join(result)
print(result)


class MyRange:
    def __init__(self, *args):
        mode = len(args)
        if mode == 1:
            self.start = 0
            self.end = args[0]
            self.step = 1
        elif mode == 2:
            self.start = args[0]
            self.end = args[1]
            self.step = 1
        elif mode == 3:
            self.start = args[0]
            self.end = args[1]
            self.step = args[2]
        else:
            raise TypeError(f"My Range awaits 1-3 arguments, was get {mode}")
        self.current = self.start

    def __iter__(self):
        return self

    def __next__(self):
        if (self.current >= self.end and self.step > 0) or (
            self.current <= self.end and self.step < 0
        ):
            raise StopIteration
        self.current += self.step
        return self.current - self.step


for i in MyRange(100, 20, -2):
    print(i)

for i in range(1, 2, 3):
    print(i)
