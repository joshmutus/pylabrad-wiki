import labrad
import time

def square_and_add(cxn, square_me, x, y):
    ss = cxn.squaring_server
    ads = cxn.addition_server
    t_start = time.time()
    
    print("Sending request to Squaring Server")
    squared = ss.square(square_me)
    t_square = time.time()
    print("Got result %f**2 = %f after %f seconds"%\
        (square_me, squared, t_square-t_start))
    
    print("Sending request to Addition Server")
    summed = ads.add(x, y)
    t_summed = time.time()
    print("Got result %d + %d = %d after %f seconds"%\
        (x, y, summed, t_summed - t_square))
    t_total = t_summed - t_start
    print("Total time taken = %f seconds."%(t_total,))
    return squared, summed
