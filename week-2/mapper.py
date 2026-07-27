def mapper(line):
    """
    Parses a record line with multiple car names separated by spaces 
    and generates (car_company, 1) for each.
    """
    words = line.strip().split()
    output = []
    
    for word in words:
        output.append((word, 1))
        
    return output