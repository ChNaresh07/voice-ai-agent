import time

def measure_latency(func):
    start = time.time()

    result = func()

    end = time.time()

    print(
        f"Latency: {(end-start)*1000:.2f} ms"
    )

    return result