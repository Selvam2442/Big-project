def reducer(key, values):
    """
    Sums all sales numbers for a given car company key.
    """
    total_sales = sum(values)
    return key, total_sales