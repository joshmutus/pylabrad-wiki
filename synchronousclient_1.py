import labrad
import time

def square_numbers(cxn, numbers):
    ss = cxn.squaring_server
    t_start = time.time()
    print("Starting synchronous requests...")
    for n in numbers:
        square = ss.square(n)
        print("%f**2 = %f"%(n, square))
    t_total = time.time() - t_start
    print("Finished %d requests after %f seconds."%(len(numbers), t_total))
