import numpy as np

def solve(A: np.ndarray, b: np.ndarray, mod=None):
    # Solve system of linear equations
    # Only returns a solution if there is a unique one, otherwise returns None
    M = np.concatenate([A, b], axis=1)
    rank = M.shape[0]
    # Gaussian elimination
    for i in range(M.shape[0]):
        failed = False
        if M[i, i] == 0:
            # Attempt to do row swapping
            failed = True
            for j in range(i+1, M.shape[0]):
                if M[j, i] != 0:
                    temp = M[i].copy()
                    M[i] = M[j]
                    M[j] = temp
                    failed = False
                    break
            if failed:
                if M[i, -1] != 0:
                    # No solution
                    return None
                
                # Multiple solutions
                rank = i
                
        if failed:
            break
        
        M[i] = M[i]/M[i, i]
        for j in range(i+1, M.shape[0]):
            M[j] -= M[j, i]*M[i]
        
        if mod is not None:
            M = M % mod

    print(rank)
    # Backward substitution
    for i in range(rank-1, 0, -1):
        for j in range(i):
            M[j] -= M[j, i]*M[i]
        
        M = M % mod
    
    return M[:, A.shape[0]]
