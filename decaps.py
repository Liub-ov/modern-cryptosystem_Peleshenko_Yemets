import numpy as np

from encaps import H, H_prime, G


def decaps(params, ciphertext, sk, pk):
    C1, C2, d = ciphertext

    # compute M' and R'
    print(sk[1].shape)
    print(C1.shape)
    M_prime = (
            np.floor(2/params['p']) * (C2 + sk[0].T @ C1) % params['p']
               ).astype(int)
    R_prime = H(params, M_prime)

    # compute d' and C1', C2'
    d_prime = H_prime(params, M_prime)
    C1_prime = (
            np.ceil(params['p']/params['q']) * pk[0].T @ R_prime % params['p']
            ).astype(int)
    C2_prime = (
            np.floor(params['p']/params['q']) *
            ((params['q']/2) * M_prime + pk[1].T @ R_prime) % params['p']
            ).astype(int)

    # reconstruct the ciphertext to check if it matches the original
    C_prime = (C1_prime, C2_prime, d_prime)

    # compute the shared key K
    if np.array_equal(ciphertext, C_prime):
        K = G(params, C1, C2, M_prime, d)
    else:
        K = G(params, C1, C2, sk[1], d)

    return K
