sentence = input("Enter a sentence: ").split(' ')
pig_latin = []
for i in sentence:
    new_word = i[1:] + i[0]
    pig_latin.append(new_word + 'ay')
print(' '.join(pig_latin))