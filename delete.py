import hashlib

cardnumber = b'2079666858888750'  # Convert the integer to bytes
hc = hashlib.sha384(cardnumber)

print(hc.hexdigest())