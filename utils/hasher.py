import hashlib

def generate_unordered_hash(word_list: list[str]) -> str:
    # Convert the list to a set to remove duplicates and make it unordered
    unordered_set = set(word_list)
    
    # Use the hashlib module to generate a hash value
    hash_object = hashlib.sha256(str(unordered_set).encode())
    hash_value = hash_object.hexdigest()
    
    return hash_value

