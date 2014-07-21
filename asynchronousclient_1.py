import labrad
import time

def square_and_add(cxn, square_me, x, y):
    ss = cxn.squaring_server
    ads = cxn.addition_server
    t_start = time.time()
    print("Sending request to Squaring Server")
    squared_future = ss.square(square_me, wait=False)
    print("Sending request to Addition Server")
    summed_future = ads.add(x, y, wait=False)
    print("Waiting for results...")
    squared = squared_future.wait()
    summed = summed_future.wait()
    print("done")
    t_total = time.time() - t_start
    print("%f**2 = %f"%(square_me, squared))
    print("%d + %d = %d"%(x, y, summed))
    print("Total time taken = %f seconds."%(t_total))
    return squared, summed
