def is_valid_brackets(s: str) -> bool:
    result = []
    backets = {"(": ")", "[": "]", "{": "}"}

    for char in s:

        if char in backets.values():
            result.append(char)

        elif char in backets:
            # if not result or backets[result.pop()] != char:
            if not result or result.pop() != backets[char]:
                return False

    return len(result) == 0


print(is_valid_brackets("(())"))
