import matplotlib.pyplot as plt

def gcd(x, y):
    i=1
    print(x+y)
    plt.plot([i], [x+y], "bo")

    while (y):
        x,y = y, x%y
        
        if (i%2 == 0):
            print(x+y)
            plt.plot([i], [x+y], 'ro')
      
        i+=1
      
    return x, (i-1)

print(gcd(55046789, 34165))
plt.show()
