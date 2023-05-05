import matplotlib.pyplot as plt
from random import choices
from pandas import DataFrame, concat

start_bigrams = {}
bigrams = {}
start_bigrams_probs = {}
bigrams_probs = {}

with open('names.txt', 'r') as f:
    names = f.read().splitlines()

for name in names:
    name = '^' + name.strip() + '$'
    for i in range(0, len(name) - 1):
        bigram = name[i] + name[i + 1]
        if i == 0:
            start_bigrams[bigram] = start_bigrams[bigram] + 1 if start_bigrams.get(bigram) else 1
            continue
        bigrams[bigram] = bigrams[bigram] + 1 if bigrams.get(bigram) else 1

for bigram, value in start_bigrams.items():
    start_bigrams_probs[bigram] = value / len(start_bigrams)
for bigram, value in bigrams.items():
    bigrams_probs[bigram] = value / len(bigrams)

names = list(bigrams_probs.keys())
weights = list(bigrams_probs.values())
names_start = list(start_bigrams_probs.keys())
weights_start = list(start_bigrams_probs.values())
table = concat([DataFrame(start_bigrams_probs.items(), columns=['start_letter', 'start_probs']), DataFrame(bigrams_probs.items(), columns=['letter', 'probs'])], axis=1)


def generate_name() -> str:
    name = choices(names_start, weights_start)[0][1]
    while True:
        letter = choices(names, weights)[0]
        name += letter[0]
        if letter[1] == '$':
            break
        name += letter[1]
    return name


def probability_visualize() -> DataFrame:
    return table


def probability_visualize_graph_img():
    fig, ax = plt.subplots()
    labels = table.start_letter + "|" + table.letter

    x = range(len(labels))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)

    ax.bar(x, table.start_probs, color='blue', label='Start')
    ax.bar(x, table.probs, bottom=table.start_probs, color='orange', label='Bigram')
    ax.legend()

    plt.title('Bigram probabilities')
    plt.xlabel('Bigram')
    plt.ylabel('Probability')
    plt.savefig('table.png')
    plt.show()


print(generate_name())
print(generate_name())
print(generate_name())
print(probability_visualize())
probability_visualize_graph_img()
