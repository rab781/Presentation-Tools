import time
try:
    import psutil
    import win32gui
    import win32process
except:
    pass

def test_fast_path(iterations=1000):
    start = time.time()
    for _ in range(iterations):
        # simulate fast path
        window_title = "google slides - presentation"
        if "google slides" in window_title:
            detected = "google_slides"
    return time.time() - start

def test_slow_path(iterations=100):
    start = time.time()
    for _ in range(iterations):
        # simulate psutil
        try:
            p = psutil.Process()
            p.name()
        except:
            pass
    return time.time() - start

print(f"Fast path (1000 iters): {test_fast_path():.4f}s")
print(f"Slow path (100 iters): {test_slow_path():.4f}s")
