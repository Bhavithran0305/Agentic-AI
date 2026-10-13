import hashlib
 
text = """
    Name: John
    Email: john@gmail.com
    Phone: 9876543210
    Aadhaar: 1234-5678-9012
    Credit Card: 4111-1111-1111-1111"""
 
print("Original Text:")
print(text)
 
# 1. Block if Credit Card Found
credit_card = "4111-1111-1111-1111"
 
if credit_card in text:
    text = text.replace(credit_card, "[BLOCKED]")
 
# 2. Hash Email
email = "john@gmail.com"
hashed_email = hashlib.sha256(email.encode()).hexdigest()
text = text.replace(email, hashed_email)
 
 
# 3. Mask Phone
phone = "9876543210"
masked_phone = "********10"
text = text.replace(phone, masked_phone)
 
 
# 4. Redact Aadhaar
aadhaar = "1234-5678-9012"
text = text.replace(aadhaar, "[REDACTED]")
 
# -------------------------------
# Final Output
# -------------------------------
print("\nProcessed Text:")
print(text)





