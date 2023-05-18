import random
import string
import collections
import math
from matplotlib import pyplot as plt


# 16-th variant input data
# 1-st Task
def lossless_comp():
    last_name = "Чуйченко"
    last_name_and_group = "Чуйченко_519ст_"
    n_1 = 16

    def parameters(s):
        counts = collections.Counter(s)
        probability = {symbol: count / n_sequence for symbol, count in counts.items()}
        probability_string = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])
        main_probability = sum(probability.values()) / len(probability)
        equality = all(abs(prob - main_probability) < 0.05 * main_probability for prob in probability.values())
        if equality == main_probability:
            uniformity = "рівна"
        else:
            uniformity = "нерівна"
        entropy = -sum(p * math.log2(p) for p in probability.values())
        if sequence_size_alphabet > 1:
            source_excess = 1 - entropy / math.log2(sequence_size_alphabet)
        else:
            source_excess = 1
        return probability_string, main_probability, uniformity, entropy, source_excess

    def output():
        text = open('results_sequence.txt', 'a')
        text.write(f'Ймовірність появи символів: {probability_str}\n')
        text.write(f'Середнє арифметичне ймовірності: {round(mean_probability, 2)}\n')
        text.write(f'Ймовірність розподілу символів: {uniformity}\n')
        text.write(f'Ентропія: {round(entropy, 2)}\n')
        text.write(f'Надмірність джерела: {round(source_excess, 2)}\n')
        text.write('\n')

    text = open('results_sequence.txt', 'w')
    n_sequence = 100
    arr1 = [1] * n_1
    n_0 = n_sequence - n_1
    arr0 = [0] * n_0
    results = []

    original_sequence_1 = arr1 + arr0
    random.shuffle(original_sequence_1)
    original_sequence_1 = ''.join(map(str, original_sequence_1))

    text.write(f'Варіант: 16\n')

    text.write(f'\nЗавдання 1\n')
    text.write('Послідовність: ' + str(original_sequence_1) + '\n')
    original_sequence_size = len(original_sequence_1)
    text.write('Розмір послідовності: ' + str(original_sequence_size) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_1)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_1)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 2-nd Task
    n_2 = 8
    list2 = [str(i) for i in last_name]
    no_2 = n_sequence - n_2
    list0_2 = ['0'] * no_2

    original_sequence_2 = list2 + list0_2
    original_sequence_2 = ''.join(map(str, original_sequence_2))

    text.write(f'\nЗавдання 2\n')
    text.write('Послідовність: ' + str(original_sequence_2) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_1)) + ' byte' + '\n')
    unique_chars_2 = set(original_sequence_2)
    sequence_size_alphabet = len(unique_chars_2)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_2)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 3-rd Task
    original_sequence_3 = list(original_sequence_2)
    random.shuffle(original_sequence_3)
    original_sequence_3 = ''.join(map(str, original_sequence_3))

    text.write(f'\nЗавдання 3\n')
    text.write('Послідовність: ' + str(original_sequence_3) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_3)) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_3)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_3)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 4-th Task
    aray = []
    letters = [str(i) for i in last_name_and_group]
    n_letters = len(letters)
    n_repeats = n_sequence // n_letters
    remainder = n_sequence % n_letters
    aray += letters * int(n_repeats)
    aray += letters[:remainder]

    original_sequence_4 = ''.join(map(str, aray))

    text.write(f'\nЗавдання 4\n')
    text.write('Послідовність: ' + str(original_sequence_4) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_4)) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_4)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_4)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 5-th Task
    alphabet = ['Ч', 'у', '5', '1', '9']
    pi = 0.2
    length = pi * n_sequence

    original_sequence_5 = alphabet * int(length)
    random.shuffle(original_sequence_5)
    original_sequence_5 = ''.join(map(str, original_sequence_5))

    text.write(f'\nЗавдання 5\n')
    text.write('Послідовність: ' + str(original_sequence_5) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_5)) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_5)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_5)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 6-th Task
    list_letters = ['Ч', 'у']
    list_digits = ['5', '1', '9']
    p_letters = 0.7
    p_digits = 0.3
    n_letters6 = int(p_letters * n_sequence) / len(list_letters)
    n_digits6 = int(p_digits * n_sequence) / len(list_digits)
    list_l = list_letters * int(n_letters6)
    list_d = list_digits * int(n_digits6)

    original_sequence_6 = list_l + list_d
    random.shuffle(original_sequence_6)
    original_sequence_6 = ''.join(map(str, original_sequence_6))

    text.write(f'\nЗавдання 6\n')
    text.write('Послідовність: ' + str(original_sequence_6) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_6)) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_6)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_6)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 7-th Task
    elements = string.ascii_lowercase + string.digits

    original_sequence_7 = [random.choice(elements) for _ in range(n_sequence)]
    original_sequence_7 = ''.join(map(str, original_sequence_7))

    text.write(f'\nЗавдання 7\n')
    text.write('Послідовність: ' + str(original_sequence_7) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_7)) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_7)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_7)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    # 8-th Task
    original_sequence_8 = ['1'] * n_sequence
    original_sequence_8 = ''.join(map(str, original_sequence_8))

    text.write(f'\nЗавдання 8\n')
    text.write('Послідовність: ' + str(original_sequence_8) + '\n')
    text.write('Розмір послідовності: ' + str(len(original_sequence_8)) + ' byte' + '\n')
    unique_chars_8 = set(original_sequence_8)
    sequence_size_alphabet = len(unique_chars_8)
    text.write('Розмір алфавіту: ' + str(sequence_size_alphabet) + '\n')

    probability_str, mean_probability, uniformity, entropy, source_excess = parameters(original_sequence_8)
    results.append([sequence_size_alphabet, round(entropy, 2), round(source_excess, 2), uniformity])

    output()

    text.close()

    seq = open('sequence.txt', 'w')
    original_sequences = [original_sequence_1, original_sequence_2, original_sequence_3, original_sequence_4,
                          original_sequence_5, original_sequence_6, original_sequence_7, original_sequence_8]
    seq.write(str(original_sequences))
    seq.close()

    text.close()

    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4', 'Послідовність 5',
           'Послідовність 6', 'Послідовність 7', 'Послідовність 8']
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig('Таблиця' + '.png')


lossless_comp()
