from datetime import datetime

def format_date(date_input):
    if isinstance(date_input, datetime):
        date_obj = date_input
    elif isinstance(date_input, str):
        date_obj = datetime.strptime(date_input, "%Y-%m-%d")
    else:
        raise TypeError("date_input must be a str or datetime.date object")

    # Extract the day, month, and year
    day = date_obj.day
    month = date_obj.strftime("%B")

    # Determine the appropriate suffix for the day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Return the formatted date string
    return f"{month} {day}{suffix}"