def format_cop(amount):
    # Ensure the amount is a float with two decimal places
    formatted_amount = f"{amount:,.2f}"

    # Add the "COP" symbol in front of the formatted amount
    return f"COP ${formatted_amount}"
