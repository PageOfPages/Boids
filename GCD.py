def gcd(x, y):
    i=1
    print(x+y)
    
    while (y!=0):
        x,y = y, (x%y)
        
        if (i%2 == 0):
            print(x+y)
      
        i+=1
      
    return x, (i-1)

print(gcd(55046789, 34165))


