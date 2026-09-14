# stress_cpu.py
while True:
    x = 0
    for i in range(1000000):
        x += i * i


print("completed")