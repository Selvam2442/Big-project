def sort_partition_data(data):
    """
    Sorts intermediate key-value pairs by key.
    """
    return sorted(data, key=lambda x: x[0])