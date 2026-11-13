
def validate_uk_vat_checksum(vat):
    # Remove spaces and convert to uppercase
    vat = vat.upper().replace(" ", "")

    # Standard UK VAT number: GB + 9 digits
    if vat.startswith("GB"):
        vat = vat[2:]

    if len(vat) != 9 or not vat.isdigit():
        return False

    digits = [int(digit) for digit in vat]

    weights = [8, 7, 6, 5, 4, 3, 2]

    total = sum(
        digits[i] * weights[i]
        for i in range(7)
    )

    check_digit = total % 97

    return check_digit == (digits[7] * 10 + digits[8])


# Test examples
test_numbers = [
    "GB245719348",
    "GB793527394",
    "GB718344334"
]

for vat in test_numbers:
    print(vat, validate_uk_vat_checksum(vat))
