import random
import time
from lruCache import LRUCache

# Глобальний екземпляр кешу (ємність K = 1000)
_cache = LRUCache(capacity=1000)


def range_sum_no_cache(array, left, right):
    total = 0
    for i in range(left, right + 1):
        total += array[i]
    return total


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right):
    key = (left, right)
    cached = _cache.get(key)
    if cached != -1:  # cache-hit
        return cached
    # cache-miss: обчислюємо суму і зберігаємо результат
    total = sum(array[left : right + 1])
    _cache.put(key, total)
    return total


def update_with_cache(array, index, value):
    array[index] = value
    # Лінійний прохід по ключах кешу — інвалідуємо всі діапазони,
    # що містять змінений index (left <= index <= right).
    keys_to_delete = [
        (left, right) for (left, right) in _cache.keys() if left <= index <= right
    ]
    for key in keys_to_delete:
        _cache.delete(key)


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]

    queries = []

    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


if __name__ == "__main__":
    N = 25_000
    Q = 12_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    # --- Без кешу ---
    arr1 = array[:]
    t0 = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(arr1, q[1], q[2])
        else:
            update_no_cache(arr1, q[1], q[2])
    t_no_cache = time.time() - t0

    # --- З LRU-кешем ---
    arr2 = array[:]
    _cache.__init__(1000)  # скидаємо кеш перед тестом
    t0 = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(arr2, q[1], q[2])
        else:
            update_with_cache(arr2, q[1], q[2])
    t_with_cache = time.time() - t0

    print(f"Без кешу:      {t_no_cache:.4f} с")
    print(
        f"LRU-кеш:        {t_with_cache:.4f} с  (прискорення ×{t_no_cache / t_with_cache:.1f})"
    )
