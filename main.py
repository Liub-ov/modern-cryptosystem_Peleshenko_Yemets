from keygen import keygen
from encaps import encaps
from decaps import decaps


# params = {
#     'm': 10,
#     'n': 6,
#     'l1': 5,
#     'l2': 5,
#     'd': 2**6,
#     'p': 3,
#     'q': 2**15,
#     'rho': 0.1,
#     'sigma': 3.19,
#     }

params = {
    'm': 1024,
    'n': 536,
    'l1': 16,
    'l2': 16,
    'd': 2**4,
    'p': 2**9,
    'q': 2**11,
    'rho': 0.1,
    'sigma': 3.19,
    }

# generate pk and sk
pk, sk = keygen(params)

print('=== public key ===')
print(pk)
print()
print('=== secret key ===')
print(sk)
print()

ciphertext, shared_key = encaps(params, pk)

print('=== ciphertext ===')
print(ciphertext)
print()
print('=== shared_key ===')
# print(shared_key)
print([x for x in shared_key])
print()

k = decaps(params, ciphertext, sk, pk)

print('=== decaps output ===')
# print(k)
print([x for x in k])
print(shared_key == k)
