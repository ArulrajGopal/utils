# stress_cpu_multi.py
import multiprocessing

def cpu_stress():
    while True:
        x = 0
        for i in range(1000000):
            x += i * i

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    print(f"Starting stress on {num_cores} CPU cores...")
    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


print("completed")
