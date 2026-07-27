import multiprocessing
import os
from mapper import mapper
from partitioner import partition
from sorter import sort_partition_data
from reducer import reducer

# Configuration settings
NUMBER_OF_REDUCERS = 2
CHUNK_SIZE = 100  # Process 500 lines per chunk to prevent CPU overload


def mapper_worker(lines):
    result = []
    for line in lines:
        mapped_values = mapper(line)
        result.extend(mapped_values)
    return result


def create_partitions(mapped_data):
    partitions = {}

    for key, value in mapped_data:
        reducer_id = partition(key, NUMBER_OF_REDUCERS)
        if reducer_id not in partitions:
            partitions[reducer_id] = []
        partitions[reducer_id].append((key, value))

    os.makedirs("intermediate", exist_ok=True)

    for reducer_id in range(NUMBER_OF_REDUCERS):
        filename = f"intermediate/partition_{reducer_id}.txt"
        data = partitions.get(reducer_id, [])
        # Sort partition data before writing to disk
        sorted_data = sort_partition_data(data)

        with open(filename, "w") as file:
            for key, value in sorted_data:
                file.write(f"{key} {value}\n")


def reducer_worker(reducer_id):
    filename = f"intermediate/partition_{reducer_id}.txt"
    if not os.path.exists(filename):
        return []

    grouped = {}
    with open(filename) as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            key = parts[0]
            value = int(parts[1])

            if key not in grouped:
                grouped[key] = []
            grouped[key].append(value)

    output = []
    for key, values in grouped.items():
        output.append(reducer(key, values))

    return output


if __name__ == "__main__":
    # Step 1: Read input file
    input_file = "input.txt"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found! Please run generate_input.py first.")
        exit(1)

    with open(input_file) as file:
        lines = file.readlines()

    print("=== Step 1: Splitting Input Data ===")
    chunks = [lines[i : i + CHUNK_SIZE] for i in range(0, len(lines), CHUNK_SIZE)]
    print(f"Split dataset into {len(chunks)} chunk(s).")

    print("\n=== Step 2: Running Mappers ===")
    # Safely limit process pool size to available CPU cores
    max_workers = min(len(chunks), multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=max_workers) as pool:
        mapper_results = pool.map(mapper_worker, chunks)

    intermediate = [pair for result in mapper_results for pair in result]
    print(f"Generated {len(intermediate)} intermediate key-value pairs.")

    print("\n=== Step 3: Partitioning & Sorting ===")
    create_partitions(intermediate)
    print("Intermediate files created in 'intermediate/' directory.")

    print("\n=== Step 4: Running Reducers ===")
    reducer_workers = min(NUMBER_OF_REDUCERS, multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=reducer_workers) as pool:
        final_output_list = pool.map(reducer_worker, range(NUMBER_OF_REDUCERS))

    print("\n=== Step 5: Final Aggregated Output ===")
    os.makedirs("output", exist_ok=True)
    output_filepath = "output/final_sales_report.txt"

    with open(output_filepath, "w") as out_file:
        for reducer_result in final_output_list:
            for company, total_sales in reducer_result:
                line_str = f"{company}: {total_sales} units sold"
                print(line_str)
                out_file.write(line_str + "\n")

    print(f"\nFinal report successfully saved to '{output_filepath}'.")