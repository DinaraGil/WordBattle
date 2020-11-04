# with open('data/freq_nouns_sorted_by_len.txt', 'r', encoding='utf-8') as file:
#     data = file.read().splitlines()
#
# data2 = []
# for word in data:
#     if 2 <= len(word) <= 6:
#         data2.append(word)
#
# with open('data/first_words.txt', 'w', encoding='utf-8') as file2:
#     for item in data2:
#         file2.write("%s\n" % item)
#
# file.close()
# file2.close()

from Level import GameLevel
from Word import Word

level = GameLevel(1).get_level()

random_index = level.get_random_index()
random_word = level.get_random_word()

bin_word_number = random_word.bin_number

attack_word_bin = Word('кот')
attack_word_bin_number = attack_word_bin.bin_number

mask = bin_word_number & attack_word_bin_number

print(mask)

