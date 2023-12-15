a = [1]

def f():
    a.append(2)
    raise Exception()

try:
    f()
except Exception:
    print("boop")

print(a)
