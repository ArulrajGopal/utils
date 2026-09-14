# stress_memory.py
import time

memory_hog = []

try:
    while True:
        memory_hog.append('A' * 10**6)  # Allocates 1MB strings repeatedly
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Stopped by user")


print("Stopped by user")