import functools, time, logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def timeit(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        t = time.perf_counter()
        r = func(*a, **kw)
        logging.info(f"  [vaqt] {func.__name__}: {time.perf_counter()-t:.4f}s")
        return r
    return wrapper

def retry(times=3):
    def dec(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            for i in range(times):
                try: return func(*a, **kw)
                except Exception as e:
                    logging.info(f"  [retry {i+1}] {e}")
            raise RuntimeError("Barcha urinishlar muvaffaqiyatsiz")
        return wrapper
    return dec

def validate(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        for v in a:
            if isinstance(v, (int,float)) and v < 0:
                raise ValueError(f"Manfiy qiymat: {v}")
        return func(*a, **kw)
    return wrapper

@timeit
@retry(times=3)
@validate
def risky_divide(a, b):
    if b == 0: raise ZeroDivisionError("Nolga bo'lish!")
    return a / b

if __name__ == "__main__":
    print(risky_divide(10, 2))

    try:
        risky_divide(10, 0)
    except RuntimeError as e:
        print(f"  {e}")

    try:
        risky_divide(-5, 2)
    except ValueError as e:
        print(f"  Xato: {e}")
