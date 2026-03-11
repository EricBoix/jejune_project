import re
s = 'I am \nstruggling to\n\n\n to make this this work'
match = re.search(r'(\n){2}(?!(\n))', s)
print("No return                   ", re.search(r'(?!(\n))', s))
print("Two returns (at least)      ", re.search(r'(\n){2}', s))
print("Exactly two, not 1 and NOT 3", re.search(r'(\n){2}(?!(\n))', s))
print("Exactly two, not 1 and NOT 3", re.search(r'(?<!(\n))(\n){2}(?!(\n))', s))
