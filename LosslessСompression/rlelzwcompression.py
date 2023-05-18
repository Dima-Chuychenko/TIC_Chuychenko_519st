import ast
import collections
import math
from matplotlib import pyplot as plt

open("results_rle_lzw.txt", "w")
results = []
N_sequence = 100


def main():
    with open("sequence.txt", "r") as file:
        original_sequence = ast.literal_eval(file.read())
        original_sequence = [sequence.strip("'[]',") for sequence in original_sequence]
        file.close()

    for row in original_sequence:
        counter = collections.Counter(row)  # count the number of occurrences of each character in the sequence
        probability = {symbol: count / N_sequence for symbol, count in counter.items()}  # calculate the probability
        entropy = -sum(p * math.log2(p) for p in probability.values())  # calculate the entropy with Shannon's formula

        # The entropy value for the sequence, as well as information about the number of bits - we save
        file = open("results_rle_lzw.txt", "a")
        file.write("////////////////////////////////////////////////\n"
                   "Оригінальна послідовність: {0}\n".format(str(row)) +
                   "Розмір оригінальної послідовності: {0} bits\n".format(str(len(row) * 16)) +
                   "Ентропія: {0}\n".format(str(round(entropy, 2))))
        file.close()

        encoded_sequence, encoded = encode_rle(row)
        decoded_sequence = decode_rle(encoded)  # the size of the coded sequence
        coded_sequence_size = len(encoded_sequence) * 16
        compression_ratio_rle = round((len(row) / len(encoded_sequence)), 2)

        if compression_ratio_rle < 1:
            compression_ratio_rle = '-'
        else:
            compression_ratio_rle = compression_ratio_rle

        file = open("results_rle_lzw.txt", "a")
        file.write("\n__________Кодування_RLE__________\n" +
                   "Закодована RLE послідовність: " + str(encoded_sequence) + "\n"
                   "Розмір закодованої RLE послідовності: " + str(round(coded_sequence_size, 2)) + " bits\n"
                   "Коефіцієнт стиснення RLE: " + str(compression_ratio_rle) + "\n"
                   "Декодована RLE послідовність: " + str(decoded_sequence) + "\n"
                   "Розмір декодованої RLE послідовності: " + str(len(decoded_sequence) * 16) + " bits\n")

        with open("results_rle_lzw.txt", "a") as file:
            file.write("\n_________Кодування_LZW_________\n"
                       "______Поетапне кодування_______\n")

        encoded_result, size = encode_lzw(row)
        with open("results_rle_lzw.txt", "a") as file:
            file.write(f"\n_______________________________________"
                       f"\nЗакодована LZW послідовність:{''.join(map(str, encoded_result))}"
                       f"\nРозмір закодованої LZW послідовності: {size} bits \n")

            compression_ratio_lzw = round((len(row) * 16 / size), 2)

            file.write(f"Коефіціент стиснення LZW: {round(compression_ratio_lzw, 2)} \n")

        decoded_result_lzw = decode_lzw(encoded_result)
        with open("results_rle_lzw.txt", "a") as file:
            file.write(f"Декодована LZW послідовність:{''.join(map(str, decoded_result_lzw))} \n"
                       f"Розмір декодованої LZW послідовності: {len(decoded_result_lzw) * 16} bits \n ")

        results.append([round(entropy, 2), compression_ratio_rle, compression_ratio_lzw])

    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    headers = ["Ентропія", "КС RLE", "КС LZW"]
    row = ["Послідовність 1", "Послідовність 2", "Послідовність 3", "Послідовність 4", "Послідовність 5",
           "Послідовність 6", "Послідовність 7", "Послідовність 8"]
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row,
                     loc="center", cellLoc="center")

    table.set_fontsize(14)
    table.scale(0.8, 2)
    ax.text(0.5, 0.95, "Результати стиснення методами RLE та LZW", transform=ax.transAxes, ha="center", va="top",
            fontsize=14)

    fig.savefig("Результати стиснення методами RLE та LZW" + ".jpg", dpi=600)


# This function returns the number of current iterations and the value of the element on the current iteration.
def encode_rle(sequence):
    result = []
    count = 1
    for i, item in enumerate(sequence):
        if i == 0:
            continue
        elif item == sequence[i - 1]:
            count += 1
        else:
            result.append((sequence[i - 1], count))
            count = 1
    result.append((sequence[len(sequence) - 1], count))

    encoded = []
    for i, item in enumerate(result):
        encoded.append(f"{item[1]}{item[0]}")

    return "".join(encoded), result


# RLE decoding
def decode_rle(sequence):
    result = []
    for item in sequence:
        result.append(item[0] * item[1])
    return "".join(result)


# The LZW algorithm is used to compress data without loss through replacement long sequences of characters per code
def encode_lzw(sequence):
    dictionary = {}
    for i in range(65536):
        dictionary[chr(i)] = i
    current = ""
    result = []
    size = 0
    for char in sequence:
        new_str = current + char
        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])
            dictionary[new_str] = len(dictionary)
            element_bits = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
            current = char
            with open("results_rle_lzw.txt", "a") as file:
                file.write(f"Code: {dictionary[current]}, Element: {current}, Bits: {element_bits}\n")
            size = size + element_bits
    last: int = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
    size = size + last
    with open("results_rle_lzw.txt", "a") as file:
        file.write(f"Code: {dictionary[current]}, Element: {current}, Bits: {last}\n")
    result.append(dictionary[current])
    return result, size


# LZW decoding
def decode_lzw(sequence):
    dictionary = {}
    for i in range(65536):
        dictionary[i] = chr(i)
    result = ""
    previous = None
    for code in sequence:
        if code in dictionary:
            current = dictionary[code]
            result += current
            if previous is not None:
                dictionary[len(dictionary)] = previous + current[0]
            previous = current
        else:
            current = previous + previous[0]
            result += current
            dictionary[len(dictionary)] = current
            previous = current
    return result


if "__main__" == __name__:
    main()
