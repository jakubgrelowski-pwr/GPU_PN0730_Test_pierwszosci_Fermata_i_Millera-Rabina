import subprocess
import time
from random import randint, choice

carmichael_numbers = [633267, 414154, 622188, 269938, 788018, 676447, 858479, 201674, 996040, 1000037]

scripts = ["miller_rabin_st.py", "miller_rabin_cpu.py", "miller_rabin_gpu.py", "../Test_Fermata/fermat_cpu_test.py", "../Test_Fermata/fermat_gpu_test.py"]

number_ranges = {
    "1001-9999": (1001, 9999),
    "10001-99999": (10001, 99999),
    "100001-999999": (100001, 999999),
    "Carmichael": carmichael_numbers
}

TEST_COUNT = 100

k = 10000

def measure_time(script, n, k):
    start = time.perf_counter()
    with subprocess.Popen(["python", script, str(n), str(k)],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as process:
      print(process.args)
      stdout, stderr = process.communicate()
      end = time.perf_counter()
    return end - start, stdout

total_times = {script: {range_name: 0 for range_name in number_ranges} for script in scripts}

for range_name, number_range in number_ranges.items():
    print(f"Zakres testu {range_name}: {number_range}")
    for script in scripts:
        print(f"Test algorytmu {script}")
        for _ in range(TEST_COUNT):
            n = randint(*number_range) if range_name != "Carmichael" else choice(carmichael_numbers)

            time_taken, result = measure_time(script, n, k)
            total_times[script][range_name] += time_taken

            print(f"Algorytm {script}, test {_+1}/{TEST_COUNT}, czas: {time_taken:.4f}s, rezultat: {result}")

        avg_time = total_times[script][range_name] / TEST_COUNT
        print(f"Średni czas wykonania {script} w zakresie {range_name}: {avg_time:.4f}s\n")

for script in scripts:
    for range_name in number_ranges:
        print(f"Całkowity czas wykonania {script} w zakresie {range_name}: {total_times[script][range_name]:.4f}s")
