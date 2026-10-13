import hashlib
 
def generate_sha256(text: str) -> str:
    # Convert string to bytes, then calculate the 256-bit hash
    encoded_bytes = text.encode("utf-8")
    sha256_hash = hashlib.sha256(encoded_bytes)
 
    # Return the hexadecimal string (64 characters)
    return sha256_hash.hexdigest()
 
 
# Example Usage
if __name__ == "__main__":
    user_input = input("Enter text to hash: ")
    hashed_output = generate_sha256(user_input)
 
    print(f"\nInput:  {user_input}")
    print(f"SHA256: {hashed_output}")
 








