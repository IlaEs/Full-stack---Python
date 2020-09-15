import time

def f0(func):

    def f1():
        NUM_RUNS = 10
        avg_time = 0

        for i in range(NUM_RUNS):
            t0 = time.time()
            #сама функция
            func()

            t1 = time.time()
            avg_time += (t1 - t0)

        avg_time /= NUM_RUNS
        print("Выполнение заняло %.5f секунд" % avg_time)
    return f1

@f0
def fibonachi():
    i1 = 1
    i2 = 1
    while i1 + i2 <= 10**1000:
        i1, i2 = i2, i1 + i2
fibonachi()
