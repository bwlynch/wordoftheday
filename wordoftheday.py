from PyDictionary import PyDictionary
from random_word import RandomWords
dictionary=PyDictionary()
r = RandomWords()

# Picks random words until one is chosen that 1) Is more than 9 characters long, 2) Is not Nonetype, 3) Has at least one defition, and 4) Has a definition longer than 20 characters (this last condition weeds out several cases where some words are seemingly missing most of their definition).
break_var = False
while break_var == False:
    temp_word = r.get_random_word()
    #print(temp_word)
    if temp_word is not None:
        if len(temp_word) > 9:
            temp_def = dictionary.meaning(temp_word, disable_errors=True)
            if temp_def is not None:
                for i in temp_def:
                    for j in temp_def[i]:
                        if len(j) > 20:
                            word = temp_word
                            break_var = True
                            

# Prints out all of the definitions for the chosen word
definition = dictionary.meaning(word)
print("Today's word is " + word + ". The definition(s) of " + word + " are:")
count = 1
for i in definition:
    print(i)
    for j in definition[i]:
        print(str(count) + ". " + j)
        count += 1
