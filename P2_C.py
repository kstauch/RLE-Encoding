#Project 2: RLE Encoding - Combined Product of A and B


import console_gfx


def to_hex_string(data):
    hex_str = ''
    dec_to_hex_dict = {15: 'f', 14: 'e', 13: 'd', 12: 'c', 11: 'b', 10: 'a'}
    for val in data:
        if val >= 10:
            hex_str += dec_to_hex_dict[val]
        else:
            hex_str += str(val)

    return hex_str


def count_runs(flat_data):
    count = 1
    run_length = 1
    prev = flat_data[0]
    for val in flat_data:
        if val != prev:
            count += 1
        else:
            run_length += 1
        if run_length >= 15:
            count += 1
            run_length = 0
        prev = val

    return count


def encode_rle(flat_data):
    int_list = []
    count = 0
    prev = flat_data[0]
    for val in flat_data:
        if val == prev:
            count += 1
            prev = val
        else:
            int_list.extend([count, prev])
            count = 1
            prev = val

        if count >= 15:
            int_list.extend([count, prev])
            count = 0
            prev = val
    int_list.extend([count, prev])

    return int_list


def get_decoded_length(rle_data):
    length = 0
    for num in rle_data[::2]:
        length += num

    return length


def decode_rle(rle_data):
    decompressed = []
    index = 0
    for multiplier in rle_data[::2]:
        temp_list = [rle_data[index + 1]]
        decompressed.extend(temp_list * multiplier)
        temp_list.clear()
        index += 2
    return decompressed


def string_to_data(data_string):
    hex_to_dec_dict = {'f': 15, 'e': 14, 'd': 13, 'c': 12, 'b': 11, 'a': 10, 'F': 15, 'E': 14, 'D': 13, 'C': 12,
                       'B': 11, 'A': 10}
    datalist = []
    for digit in data_string:
        if digit in hex_to_dec_dict:
            datalist.append(hex_to_dec_dict[digit])
        else:
            datalist.append(int(digit))

    return datalist


def to_rle_string(rle_data):
    dec_to_hex_dict = {15: 'f', 14: 'e', 13: 'd', 12: 'c', 11: 'b', 10: 'a'}
    result = ''
    end_of_list = False
    for index, element in enumerate(rle_data):
        if index == len(rle_data) - 1:  # to not add delimiter to end of string
            end_of_list = True
        if index % 2 == 0:  # every odd element (run length)
            result += str(element)
        else:  # every even element (run value)
            if element >= 10:
                result += dec_to_hex_dict[element]
            else:
                result += str(element)
            if end_of_list is False:
                result += ":"

    return result


def string_to_rle(rle_string):
    hex_to_dec_dict = {'f': 15, 'e': 14, 'd': 13, 'c': 12, 'b': 11, 'a': 10, 'F': 15, 'E': 14, 'D': 13, 'C': 12,
                       'B': 11, 'A': 10}
    result: list = []
    rle_string += ":"

    while len(rle_string) > 0:
        delim_index = rle_string.find(":")

        if len(rle_string[0:delim_index]) == 2:
            run_len = int(rle_string[0])
            result.append(run_len)

            if rle_string[1] in hex_to_dec_dict:
                run_val = hex_to_dec_dict[rle_string[1]]
            else:
                run_val = int(rle_string[1])
            result.append(run_val)

        else:
            run_len = int(rle_string[0] + rle_string[1])
            result.append(run_len)

            if rle_string[2] in hex_to_dec_dict:
                run_val = hex_to_dec_dict[rle_string[2]]
            else:
                run_val = int(rle_string[2])
            result.append(run_val)

        rle_string = rle_string[delim_index + 1:]

    return result


def main():

    print('''Welcome to the RLE image encoder!

Displaying Spectrum Image:''')
    console_gfx.display_image(console_gfx.test_rainbow)

    while True:

        option = input('''\nRLE Menu
--------
0. Exit
1. Load File
2. Load Test Image
3. Read RLE String
4. Read RLE Hex String
5. Read Data Hex String
6. Display Image
7. Display RLE String
8. Display Hex RLE Data
9. Display Hex Flat Data

Select a Menu Option: ''')

        if option == '0':
            break

        elif option == '1':
            filename = input("Enter name of file to load: ")
            image_data = console_gfx.load_file(filename)

        elif option == '2':
            image_data = console_gfx.test_image
            print('Test image data loaded.')

        elif option == '3':
            input_data = input("Enter an RLE string to be decoded: ")
            image_data = decode_rle(string_to_rle(input_data))

        elif option == '4':
            input_data = input("Enter the hex string holding RLE data: ")
            image_data = decode_rle(string_to_data(input_data))

        elif option == '5':
            image_data = input("Enter the hex string holding flat data: ")

        elif option == '6':
            print("Displaying image...")
            console_gfx.display_image(image_data)

        elif option == '7':
            rle_string = to_rle_string(encode_rle(image_data))
            print(f"RLE representation: {rle_string}")

        elif option == '8':
            rle_hex_string = to_hex_string(encode_rle(image_data))
            print(f"RLE hex values: {rle_hex_string}")

        elif option == '9':
            flat_data = ''
            for element in image_data:
                flat_data += str(element)
            print(f"Flat hex values: {flat_data}")

        else:
            print("Invalid Input!")


if __name__ == '__main__':
    main()