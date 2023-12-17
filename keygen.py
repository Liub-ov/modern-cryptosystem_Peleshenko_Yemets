import numpy as np


def discrete_gaussian(sigma, size):
    while True:
        continuous = np.random.normal(0, sigma, size)
        discrete = np.round(continuous)

        probability = lambda x: np.exp(-x ** 2 / (2 * sigma ** 2))
        continuous_probability = probability(continuous)
        discrete_probabilty = probability(discrete)

        threshold = np.random.uniform(0, continuous_probability)

        if np.all(discrete_probabilty < threshold):
            continue

        return discrete.astype(int)


def sample_ZOn(size, rho):
    sample = np.random.choice(
            [1, 0, -1],
            size=size,
            p=[rho/2, 1 - rho, rho/2],
            )
    return sample


def keygen(params={
        'm': 10,
        'n': 6,
        'l1': 5,
        'l2': 5,
        'd': 2**6,
        'p': 3,
        'q': 2**15,
        'rho': 0.1,
        'sigma': 3.19,
        }):
    # step 1: generate matrix A
    A = np.random.randint(0, params['q'], size=(params['m'], params['n']))

    # step 2
    S = sample_ZOn((params['n'], params['l1']), params['rho'])

    # step 3: generate matrix T and E
    T = np.random.randint(
            0,
            2,
            size=(params['l1'], params['l2']),
            )
    E = discrete_gaussian(params['sigma'],
                          (params['m'], params['l1']))

    # print('=== Matrix A ===')
    # print(A)
    # print('=== Matrix S ===')
    # print(S)
    # print('=== Matrix T ===')
    # print(T)
    # print('=== Matrix E ===')
    # print(E)

    # step 4: compute matrix B
    B = (-A @ S + E) % params['q']

    # step 5: output the keys
    # public_key = np.append(A.reshape(A.size), B.reshape(B.size))
    public_key = (A, B)
    secret_key = (S, T)

    # print('=== public key ===')
    # print(public_key)
    # print('=== secret key ===')
    # print(secret_key)

    return public_key, secret_key


if __name__ == '__main__':
    keygen()
