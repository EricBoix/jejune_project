import re

fail_one = "bulls\n\n\n         OceanofPDF.com"  # NOK: starts with small caps
fail_two = "BULLS\n\n         OceanofPDF.com"  # NOK: only two returns
fail_three = "BULLS\n\n         OceAnofPDF.com"  # NOK: wrong ending string
chap_one = "10\nBULLS\n\n\n         OceanofPDF.com"  # OK (match)
chap_two = "THE GATELESS GATE\n\n\n        OceanofPDF.com"
pattern = r"([A-Z]+(?<!(\n))(\n){3}(?!(\n))( *){8}OceanofPDF[.]com)"
print("Try matching")
print(" - a bunch of capital letters, followed by")
print(" - exactly three returns, followed by")
print(" - at least 8 white spaces, followed by")
print(" - a specific string (OceanofPDF.com)")
print("with the regex: ", pattern)

print(
    "Expected to fail, on string: ",
    repr(fail_one),
    re.search(pattern, fail_one),
)
print(
    "Expected to fail, on string: ",
    repr(fail_two),
    re.search(pattern, fail_one),
)
print(
    "Expected to fail, on string: ",
    repr(fail_three),
    re.search(pattern, fail_one),
)
print(
    "Expected to succeed on title of chapter one: ",
    repr(chap_one),
    re.search(pattern, chap_one),
)
print(
    "Expected to succeed on title of chapter two: ",
    repr(chap_two),
    re.search(pattern, chap_two),
)
