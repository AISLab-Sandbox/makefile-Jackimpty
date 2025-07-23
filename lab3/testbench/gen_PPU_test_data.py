import random

TB = 0

def main():
    data_file_path = f'./PPU_test_data/tb{TB}.txt'

    if TB == 0:
        scaling_factor = 8
    elif TB == 1:
        scaling_factor = 9
    else:
        scaling_factor = 23

    # Write the scaling factor to the input file
    with open(data_file_path, 'w') as file:
        file.write(f'{scaling_factor}\n')

    # Generate 40 random data
    if TB == 0:
        random_data = [random.randint(-65536, 65535) for _ in range(40)]
    elif TB == 1:
        random_data = [random.randint(-65536, 65535) for _ in range(40)]
    else:
        random_data = [random.randint(-2147483648, 2147483647) for _ in range(40)]

    # Write the random data to the input file
    with open(data_file_path, 'a') as file:
        file.write(','.join(map(str, random_data)))

    golden_file_path = f'./PPU_test_data/tb{TB}_golden.txt'



    print(f'Scaling Factor: {scaling_factor}')
    print(f'Data In: {random_data}')

    golden_data = []
    count = 0
    max = 0
    for value in random_data:
        if (TB == 0):
            temp = (value >> scaling_factor) + 128
            if temp > 255:
                golden_data.append(255)
            elif temp > 128:
                golden_data.append(temp)
            else:
                golden_data.append(128)
        else:
            if count == 3:
                if value > max:
                    max = value
                golden = (max >> scaling_factor) + 128
                if (golden > 255): golden = 255
                golden_data.append(golden)
                count = 0
                max = 0  # Minimum value for a 32-bit integer
            else:
                if value > max:
                    max = value
                count += 1


    with open(golden_file_path, 'w') as file:
        file.write(','.join(map(str, golden_data)))

if __name__ == "__main__":
    main()