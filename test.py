import rsa

# generate public-private key pair for the dictionary
dictionary_key_pair = rsa.newkeys(512)

# dictionary's private key
dictionary_private_key = dictionary_key_pair[1]

# member public keys
member_public_keys = {
    "member1": rsa.PublicKey(1234567890, 65537),
    "member2": rsa.PublicKey(9876543210, 65537)
}

# encrypt dictionary's private key for each member
encrypted_private_keys = {}
for member, public_key in member_public_keys.items():
    encrypted_private_key = rsa.encrypt(dictionary_private_key.save_pkcs1(), public_key)
    encrypted_private_keys[member] = encrypted_private_key

print(encrypted_private_keys)
