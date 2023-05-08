import ast
import collections
import math
import matplotlib.pyplot as plt


def main():
    results = []
    with open("sequence.txt", "r") as file:
        original_sequences = ast.literal_eval(file.read())
    for sequence in original_sequences:
        sequence = sequence[:10]
        sequence_length = len(sequence)
        unique_chars = set(sequence)
        sequence_alphabet_size = len(unique_chars)
        counts = collections.Counter(sequence)
        probability = {symbol: count / sequence_length for symbol, count in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probability.values())
        file = open("results_AC_CH.txt", "w")
        file.write(f'/' * 100)
        file.write(f'\nОригінальна послідовність: {sequence}\n')
        file.write(f'Ентропія: {entropy}\n')
        encoded_data_ac, encoded_sequence_ac = encode_ac(unique_chars, probability, sequence_alphabet_size, sequence)
        bps_ac = len(encoded_sequence_ac) / sequence_length
        decoded_sequence_ac = decode_ac(encoded_data_ac, sequence_length)
        encoded_data_hc, encoded_sequence_hc = encode_hc(unique_chars, probability, sequence)
        bps_hc = len(encoded_sequence_hc) / sequence_length
        decoded_sequence_hc = decode_hc(encoded_data_hc, sequence)
        file.write('\n' + '_' * 10 + 'Арифметичне кодування' + '_' * 10)
        file.write(f'\nДані закодованої АС послідовності: {encoded_data_ac}\n')
        file.write(f'Закодована АС послідовність: {encoded_sequence_ac}\n')
        file.write(f'Значення bps при кодуванні АС: {bps_ac}\n')
        file.write(f'Декодована АС послідовність: {decoded_sequence_ac}\n')
        file.write('\n' + '_' * 10 + 'Кодування Хаффмана' + '_' * 10)
        file.write(f'\nДані закодованої HС послідовності: {encoded_data_hc}\n')
        file.write(f'Закодована HС послідовність: {encoded_sequence_hc}\n')
        file.write(f'Значення bps при кодуванні HС: {bps_hc}\n')
        file.write(f'Декодована HС послідовність: {decoded_sequence_hc}\n')
        results.append([round(entropy, 2), bps_ac, bps_hc])
    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    headers = ['Ентропія', 'bps AC', 'bps CH']
    row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4', 'Послідовність 5',
           'Послідовність 6', 'Послідовність 7', 'Послідовність 8']
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.auto_set_font_size(True)
    table.set_fontsize(14)
    table.scale(0.6, 2.2)
    fig.savefig('Результати стиснення методами AC та CH' + '.jpg', dpi=300)


def fl_bins(point, size_cod):
    binary_code = ""
    for x in range(size_cod):
        point = point * 2
        if point > 1:
            binary_code = binary_code + str(1)
            x = int(point)
            point = point - x
        elif point < 1:
            binary_code = binary_code + str(0)
        elif point == 1:
            binary_code = binary_code + str(1)
    return binary_code


def encode_ac(uniq_chars, probabilitys, alphabet_size, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]
    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range = probability_range + probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])
    for symbol in sequence[:-1]:
        for j in range(len(unity)):
            if symbol == unity[j][0]:
                probability_low = unity[j][1]
                probability_high = unity[j][2]
                diff = probability_high - probability_low
                for k in range(len(unity)):
                    unity[k][1] = probability_low
                    unity[k][2] = probability[k] * diff + probability_low
                    probability_low = unity[k][2]
                break
    low = 0
    high = 0
    for i in range(len(unity)):
        if unity[i][0] == sequence[-1]:
            low = unity[i][1]
            high = unity[i][2]
    point = (low + high) / 2
    size_cod = math.ceil(math.log((1 / (high - low)), 2) + 1)
    bin_code = fl_bins(point, size_cod)
    return [point, alphabet_size, alphabet, probability], bin_code


def decode_ac(encoded_data_ac, sequence_length):
    point, alphabet_size, alphabet, probability = encoded_data_ac
    unity = [[alphabet[i], sum(probability[:i]), sum(probability[:i + 1])] for i in range(alphabet_size)]
    decoded_sequence = ""
    for i in range(int(sequence_length)):
        for symbol, prob_low, prob_high in unity:
            if prob_low < point < prob_high:
                diff = prob_high - prob_low
                decoded_sequence += symbol
                for j in range(alphabet_size):
                    _, prob_l, prob_h = unity[j]
                    unity[j][1], unity[j][2] = prob_low, probability[j] * diff + prob_low
                    prob_low = unity[j][2]
                break
    return decoded_sequence


def encode_hc(uniq_chars, probabilitys, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]
    final = [[alphabet[i], probability[i]] for i in range(len(alphabet))]
    final.sort(key=lambda x: x[1])
    if 1 in probability and len(set(probability)) == 1:
        symbol_code = [[alphabet[i], "1" * i + "0"] for i in range(len(alphabet))]
        encode = "".join([symbol_code[alphabet.index(c)][1] for c in sequence])
    else:
        tree = []
        for _ in range(len(final) - 1):
            left = final.pop(0)
            right = final.pop(0)
            tot = left[1] + right[1]
            tree.append([left[0], right[0]])
            final.append([left[0] + right[0], tot])
            final.sort(key=lambda x: x[1])
        symbol_code = []
        tree.reverse()
        alphabet.sort()
        for i in range(len(alphabet)):
            code = ""
            for j in range(len(tree)):
                if alphabet[i] in tree[j][0]:
                    code += '0'
                    if alphabet[i] == tree[j][0]:
                        break
                else:
                    code += '1'
                    if alphabet[i] == tree[j][1]:
                        break
            symbol_code.append([alphabet[i], code])
        encode = "".join(
            [symbol_code[i][1] for i in range(len(alphabet)) if symbol_code[i][0] == c][0] for c in sequence)
    return [encode, symbol_code], encode


def decode_hc(encoded_sequence, sequence):
    encode = list(encoded_sequence[0])
    symbol_code = encoded_sequence[1]
    count = 0
    flag = 0
    for i in range(len(encode)):
        for j in range(len(symbol_code)):
            if encode[i] == symbol_code[j][1]:
                sequence += str(symbol_code)
                flag = 1
        if flag == 1:
            flag = 0
        else:
            count += 1

            if count == len(encode):
                break
            else:
                encode.insert(i + 1, str(encode[i] + encode[i + 1]))
                encode.pop(i + 2)
    return sequence


if __name__ == "__main__":
    main()
