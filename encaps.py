import hashlib
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def serialize_matrix(M):
    return M.flatten().tobytes()


def H(params, M):
    hash_function = hashlib.sha256()
    hash_function.update(serialize_matrix(M))
    digest = hash_function.digest()
    num_bytes_needed = params['l2'] * params['m']
    R = np.frombuffer(digest * (num_bytes_needed // len(digest) + 1), dtype=np.uint8)[:num_bytes_needed]
    R = R.reshape(params['m'], params['l2']) % params['q']
    return R


def H_prime(params, M):
    hash_function = hashlib.sha256()
    hash_function.update(serialize_matrix(M))
    digest = hash_function.digest()
    l = params['l1'] * params['l2']
    num_bytes_needed = l
    d = np.frombuffer(digest * (num_bytes_needed // len(digest) + 1), dtype=np.uint8)[:num_bytes_needed]
    d = d.reshape(l) % params['p']
    return d


def G(params, C1, C2, M, d):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=params['d'] // 8,  # convert bit length to byte length
        salt=None,
        info=b'lizard_kem_context',
    )
    input_data = serialize_matrix(C1) + serialize_matrix(C2) + serialize_matrix(d) + serialize_matrix(M)
    return hkdf.derive(input_data)


def encaps(params, pk):
    M = np.random.randint(0, 2,
                          size=(params['l1'], params['l2']))

    R = H(params, M)
    d = H_prime(params, M)

    C1 = np.round(
            (params['p']/params['q']) *
            pk[0].T @ R % params['p']
            ).astype(int)
    C2 = np.round(
            (params['p']/params['q']) *
            (pk[1].T @ R + (params['q']/2) * M) % params['p']
            ).astype(int)

    K = G(params, C1, C2, M, d)

    return (C1, C2, d), K
