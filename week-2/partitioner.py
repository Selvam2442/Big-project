def partition(key, number_of_reducers):
    """
    Determines the reducer index for a given car company key using hash partitioning.
    """
    return hash(key) % number_of_reducers