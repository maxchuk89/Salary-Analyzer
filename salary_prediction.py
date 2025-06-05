def predict_salary_from_range(start, end):
    if start and end:
        return (start + end) / 2
    if start:
        return start * 1.2
    if end:
        return end * 0.8
    return None
