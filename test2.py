from pymorphy2 import MorphAnalyzer

# with open('data/nouns_from_pymorphy.txt', 'r', encoding='utf-8') as file:
#     data = file.read().splitlines()

#data = sorted(data, key=len)

# print(len(data))

morph = MorphAnalyzer()

# for word in data:

word = input()
parsed_word = morph.parse(word)[0]

tags = parsed_word.tag

print(parsed_word.tag)

stack_list_zero = list(map(str, list(parsed_word.methods_stack[0])))
stack_list_full = list(map(str, list(parsed_word.methods_stack)))

print(stack_list_full)

if '<FakeDictionary>' in stack_list_zero or '<UnknAnalyzer>' in stack_list_zero:
    print('fake')

if 'NOUN' not in tags:
    print('not noun')

bullshit_marks = ['Abbr', 'Orgn', 'Surn', 'Patr', 'Geox', 'Name', 'Trad']
for mark in bullshit_marks:
    if mark in tags:
        print('bullshit')

if 'Subx' in tags:
    print('subx')


if len(stack_list_full) >= 2:
    print('long stack')





#     if word in data:
#         if '-' in word:
#             del data[data.index(word)]
#             print('тире', word)
# #
#     if word in data:
#         if not word.isalpha():
#             del data[data.index(word)]
#     #        print('тире', word)
#
#     if word in data:
#         if len(parsed_word.methods_stack) >= 2:
#             del data[data.index(word)]
#    #         print('многа', word)
#
#     if word in data:
#         if 'Name' in parsed_word.tag:
#             del data[data.index(word)]
#   #          print('имя', word)
#
#     if word in data:
#         if 'NOUN' not in parsed_word.tag:
#             del data[data.index(word)]
#  #           print('не сущ', word)
#
#     if word in data:
#         if word.replace('ё', 'е') != parsed_word.normal_form.replace('ё', 'е'):
#             del data[data.index(word)]
# #            print('ненорм', word)

# print(len(data))
#
# with open('data/nouns_from_pymorphy.txt', 'w', encoding='utf-8') as file2:
#     for item in data:
#         file2.write("%s\n" % item)
#
# file.close()
# file2.close()
