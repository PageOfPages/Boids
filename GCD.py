import matplotlib.pyplot as plt

def gcd(x, y):
    i=1
    print(x+y)
    points = {i:x+y}
    
    while (y):
        x,y = y, x%y
        
        if (i%2 == 0):
            print(x+y)
            points[i] = x+y
      
        i+=1
    
    plt.plot(list(points.keys()), list(points.values()))
    return x, (i-1)

print(gcd(55046789, 34165))
plt.show()
