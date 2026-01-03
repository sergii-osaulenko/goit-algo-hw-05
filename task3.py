import timeit


def boyer_moore(text, pattern):
    if not pattern or not text:
        return -1

    # побудова таблиці зсувів (bad character rule)
    skip = {}
    m = len(pattern)
    for i in range(m - 1):
        skip[pattern[i]] = m - i - 1

    i = 0
    n = len(text)

    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        else:
            char = text[i + m - 1]
            i += skip.get(char, m)
    return -1


def kmp_build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    if not pattern:
        return -1

    lps = kmp_build_lps(pattern)
    i = j = 0  # i – індекс у text, j – у pattern

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp(text, pattern, base=256, mod=10**9 + 7):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return -1

    h = pow(base, m - 1, mod)
    p_hash = 0
    t_hash = 0

    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * h) % mod
            t_hash = (t_hash * base + ord(text[i + 1 + m - 1])) % mod
            t_hash = (t_hash + mod) % mod
    return -1


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def benchmark(search_fn, text, pattern, number=100):
    timer = timeit.Timer(lambda: search_fn(text, pattern))
    return timer.timeit(number=number)


def main():
    text1 = read_file("article1.txt")
    text2 = read_file("article2.txt")

    # Вибераємо реальні підрядки з текстів, наприклад перші 20–30 символів.
    existing_pat1 = text1[:30]
    existing_pat2 = text2[:30]

    fake_pat1 = "qwertyuiop1234567890"  # Точно вигаданий
    fake_pat2 = "zxcasdqwe0987654321"

    algorithms = [
        ("Boyer-Moore", boyer_moore),
        ("KMP", kmp_search),
        ("Rabin-Karp", rabin_karp),
    ]

    results = []

    for name, fn in algorithms:
        t = benchmark(fn, text1, existing_pat1)
        results.append(("article1", "existing", name, t))
        t = benchmark(fn, text1, fake_pat1)
        results.append(("article1", "fake", name, t))

        t = benchmark(fn, text2, existing_pat2)
        results.append(("article2", "existing", name, t))
        t = benchmark(fn, text2, fake_pat2)
        results.append(("article2", "fake", name, t))

    # Вивід у форматі таблиці для Markdown
    print("| Text      | Pattern   | Algorithm   | Time (sec, 100 runs) |")
    print("|-----------|-----------|------------|----------------------|")
    for text_name, kind, algo_name, t in results:
        print(f"| {text_name} | {kind} | {algo_name} | {t:.6f} |")


if __name__ == "__main__":
    main()