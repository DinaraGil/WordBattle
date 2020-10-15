with open('data/freq_nouns_sorted_by_len.txt', 'r', encoding='utf-8') as file:
    data = file.read().splitlines()

data2 = []
for word in data:
    if 2 <= len(word) <= 6:
        data2.append(word)

with open('data/first_words.txt', 'w', encoding='utf-8') as file2:
    for item in data2:
        file2.write("%s\n" % item)

file.close()
file2.close()