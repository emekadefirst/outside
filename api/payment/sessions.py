import random
import string


def generate_ticket_code(length=8, used_codes=set()):
    """Generates a random, unique ticket code."""
    while True:
        ticket_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=length)
        )
        if ticket_code not in used_codes:
            used_codes.add(ticket_code)
            return ticket_code

print(generate_ticket_code())