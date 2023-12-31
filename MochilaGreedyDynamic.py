def Greedy(wt, val, W, n):
 
    # base conditions
    if n == 0 or W == 0:
        return 0
    if t[n][W] != -1:
        return t[n][W]
 
    # choice diagram code
    if wt[n-1] <= W:
        t[n][W] = max(
            val[n-1] + Greedy(
                wt, val, W-wt[n-1], n-1),
            Greedy(wt, val, W, n-1))
        return t[n][W]
    elif wt[n-1] > W:
        t[n][W] = Greedy(wt, val, W, n-1)
        return t[n][W]
 
# Driver code
if __name__ == '__main__':
    #(15, 30), (10, 25), (2, 2), (4, 6), (6, 15), (7, 20), (20, 38)
    profit = [30, 25, 2, 6, 15, 20, 38]
    weight = [15, 10, 2, 4, 6, 7, 20]
    W = 20
    n = len(profit)
     
    # We initialize the matrix with -1 at first.
    t = [[-1 for i in range(W + 1)] for j in range(n + 1)]
    print('Guloso: ',(Greedy(weight, profit, W, n)))