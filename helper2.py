import allWords
import time
import math


ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


def remove_dups(lst):
    no_dups = []
    for e in lst:
        if e not in no_dups:
            no_dups.append(e)
    no_dups.sort()
    return no_dups


def bold_text(txt):
    print("#" * (len(txt) + 4))
    print("# " + txt + " #")
    print("#" * (len(txt) + 4))


def has_double_letters(word):
    letters = []
    for letter in word:
        if letter in letters:
            return True
        else:
            letters.append(letter)
    return False


def filter_words(words, word_len, double_letters):
    filtered_words = []
    for word in words:
        if len(word) == word_len and not (
            not double_letters and has_double_letters(word)
        ):
            filtered_words.append(word)
    return filtered_words


def get_words():
    only_common = input_yes_or_no("Only common words [Y/n]? ")
    if only_common:
        only_wordle = input_yes_or_no("Only wordle words [Y/n]? ")
        if only_wordle:
            return allWords.get_wordle_words()
        return allWords.get_common_words()
    return allWords.get_all_words()


def input_yes_or_no(prompt):
    try:
        user_input = input(prompt)
        if user_input[0].lower() == "n":
            return False
    except:
        pass
    return True


def input_word_len():
    print("How many letters are in the word?")
    while True:
        try:
            user_input = input("Length: ")
            num = int(user_input)
            assert num > 0 and num <= len(ALPHABET)
            return num
        except:
            print("Hint: enter a positive number!")


def input_green_letters(word_len, gls):
    print("Enter letters that you know the position of (aka the 'green' letters).")
    if len(gls) > 0:
        saved_letters = ""
        for i in range(word_len):
            letter_to_add = "?"
            for j in range(len(gls)):
                if i == gls[j][1]:
                    letter_to_add = gls[j][0].upper()
                    break
            saved_letters += letter_to_add
        print("Current saved green letters: '%s'" % saved_letters)
        keep_gls = input_yes_or_no(
            "Would you like to add on to/keep last enter green letters [Y/n]? "
        )
        if not keep_gls:
            gls = []
    print(
        "First enter the letter, hit [enter] then enter the position of the letter where 1 is the first letter."
    )
    while True:
        try:
            user_input = input("Letter (leave blank to continue): ")
            if len(user_input) == 0:
                return gls
            letter = user_input.lower()[0]
            assert letter in ALPHABET
            user_input = input("Position: ")
            idx = int(user_input)
            assert idx > 0 and idx <= word_len
            gls.append([letter, idx - 1])
            print("")
        except:
            print("Hint: you are doing something wrong (maybe read the directions?)")


def input_yellow_letters(word_len):
    print("Enter letters that you are are in the word (aka the 'yellow' letters).")
    print(
        "First enter the letter, hit [enter] then enter the positions where the letter is not of the letter where 1 is the first letter."
    )
    print(
        """ Example:
    Letter (leave blank to continue): r
    Position(s) where it is not: 1 3\n"""
    )
    yls = []
    while True:
        try:
            user_input = input("Letter (leave blank to continue): ")
            if len(user_input) == 0:
                return yls
            letter = user_input.lower()[0]
            assert letter in ALPHABET
            user_input = input("Position(s) where it is not: ")
            positions = user_input.split(" ")
            idxs = []
            for pos in positions:
                idx = int(pos)
                assert idx > 0 and idx <= word_len
                idxs.append(idx - 1)
            yls.append([letter, idxs])
            print("")
        except:
            print("Hint: you are doing something wrong (maybe read the directions?)")


def input_dark_letters(prompt, dls):
    print(prompt)
    if len(dls) > 0:
        saved_dls = ", ".join(dls)
        print("Current saved letters that not in the word: '%s'" % saved_dls)
        keep_letters = input_yes_or_no(
            "Would you like to add on to/keep last entered letters that are not in the word [Y/n]? "
        )
        if not keep_letters:
            dls = []
    try:
        user_input = input("Letters (ex: 'dia' without the ''s): ")
        letters_input = user_input.lower()
        for letter in letters_input:
            assert letter in ALPHABET
            dls.append(letter)
        return dls
    except:
        print("Hint: you are doing something wrong (enter only letters)")


def is_good_word(word, gls, yls, dls):
    letter_lst = list(word)
    for gl in gls:
        if word[gl[1]] == gl[0]:
            letter_lst.remove(gl[0])
        else:
            return False, letter_lst
    for yl in yls:
        if yl[0] not in letter_lst:
            return False, letter_lst
        for idx in yl[1]:
            if word[idx] == yl[0]:
                return False, letter_lst
        letter_lst.remove(yl[0])
    for dl in dls:
        if dl in letter_lst:
            return False, letter_lst
    return True, letter_lst


def run(words, gls, yls, dls):
    print("\nENTER INFORMATION...\n")

    gls = input_green_letters(len(words[0]), gls)
    print("\n")
    yls = input_yellow_letters(len(words[0]))
    print("\n")
    dls = input_dark_letters("Enter letters that are not in the word.", dls)

    print("\nSEARCHING...")
    possible_words = calc_best_words(words, gls, yls, dls)
    print("FINISHED SEARCHING...\n")

    if len(possible_words) == 1:
        bold_text("The word is: %s" % possible_words[0][0])
    elif len(possible_words) > 0:
        bold_text("Possible Words:")

        extra_letters = []
        for i in range(len(possible_words) - 1, -1, -1):
            print("%i) %s" % (i + 1, possible_words[i][0]))
            extra_letters += possible_words[i][1]

        extra_letters = remove_dups(extra_letters)
        print("\nLetters worth finding out more (the white/unused letters):")
        letter_str = ", ".join(extra_letters)
        print(letter_str)
    else:
        print("No words found. Did you mis-type or incorrectly enter information?")


# def calc_letter_counts(word_len, words, double_letters):
#     letter_counts = []
#     for i in range(len(ALPHABET)):
#         temp = [0] * word_len
#         letter_counts.append([0, temp])

#     for word in words:
#         if is_good_word(word, word_len, double_letters, [], [], [])[0]:
#             for i in range(len(word)):
#                 letter_counts[ALPHABET.index(word[i])][0] += 1
#                 letter_counts[ALPHABET.index(word[i])][1][i] += 1
#     return letter_counts


# def calc_possible_words(words, word_len, double_letters, gls, yls, dls, letter_counts):
#     word_scores = []
#     for word in words:
#         good_word = is_good_word(word, word_len, double_letters, gls, yls, dls)
#         if good_word[0]:
#             score = 0
#             for i in range(len(word)):
#                 score += letter_counts[ALPHABET.index(word[i])][0] * YELLOW_WEIGHT
#                 score += letter_counts[ALPHABET.index(word[i])][1][i] * GREEN_WEIGHT
#             if has_double_letters(word):
#                 score *= DOUBLE_LETTER_WEIGHT
#             word_scores.append([word, good_word[1], score])
#     for i in range(len(word_scores)):
#         for j in range(len(word_scores) - i - 1):
#             if word_scores[j][2] < word_scores[j + 1][2]:
#                 word_scores[j], word_scores[j + 1] = word_scores[j + 1], word_scores[j]
#     return word_scores


def wordle_compare(answer, guess):
    # letter_lst = list(word)
    # for gl in gls:
    #     if word[gl[1]] == gl[0]:
    #         letter_lst.remove(gl[0])
    #     else:
    #         return False, letter_lst
    # for yl in yls:
    #     if yl[0] not in letter_lst:
    #         return False, letter_lst
    #     for idx in yl[1]:
    #         if word[idx] == yl[0]:
    #             return False, letter_lst
    #     letter_lst.remove(yl[0])
    # for dl in dls:
    #     if dl in letter_lst:
    #         return False, letter_lst
    # return True, letter_lst
    # ARE THEY BACKWARDS? ONLY THINKG THT WOULD CHANGE IS THE DLS
    letter_lst = list(answer)
    gls = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            gls.append([guess[i], i])
            letter_lst.remove(guess[i])
    yls = []
    for i in range(len(guess)):
        if guess[i] in letter_lst:
            yls.append([guess[i], [i]])
            letter_lst.remove(guess[i])
    dls = letter_lst

    return gls, yls, dls


def calc_best_words(words):
    print("\nSTARTING CALCULATIONS...")
    t0 = time.time()
    # Once this works: guess_words should be unfiltered and answer/possible should be filtered

    # THIS MIGHT WORK, BUT IT TAKES FOREVER, SO IDK IF IT WORKS
    """
    word_scores = {}
    i = 0
    for guess_word in words:
        i += 1
        start_time = time.time()

        word_scores[guess_word] = 0
        for answer_word in words:
            gls, yls, dls = wordle_compare(guess_word, answer_word)
            for possible_valid_word in words:
                word_scores[guess_word] += not is_good_word(possible_valid_word, gls, yls, dls)[0]
        word_scores[guess_word] = word_scores[guess_word] / (len(words) ** 2) * 100 # covert to average percent invalidated

        time_taken = time.time() - start_time
        print("%i/%i: %.3f \t %s \t %i \t %.2f" % (i, len(words), i/len(words), guess_word, word_scores[guess_word], time_taken))
    """

    # THIS MIGHT ALSO WORK, but its still words^3 and takes forever
    # Uses https://www.youtube.com/watch?v=v68zYyaEmEA video's math
    # But I don't actually understand the implementation of the math in the video
    # WAIT ITS ALL WRONG
    """
    word_scores = {}
    i = 0
    for guess_word in words:
        i += 1
        start_time = time.time()

        word_scores[guess_word] = 0
        for answer_word in words:
            gls, yls, dls = wordle_compare(guess_word, answer_word)
            not_valid = 0
            for possible_valid_word in words:
                not_valid += not is_good_word(possible_valid_word, gls, yls, dls)[0]
            try:
                word_scores[guess_word] += ((len(words) - not_valid) / len(words)) * -math.log((len(words) - not_valid) / len(words), 2)
            except:
                pass

        time_taken = time.time() - start_time
        print(
            "%i/%i: %.2f \t %s \t %.2f \t %.2f"
            % (
                i,
                len(words),
                i / len(words) * 100,
                guess_word,
                word_scores[guess_word],
                time_taken,
            )
        )
    """

    # ANOTHER ATTEMPT OF THE MATH FROM THE VIDEO
    # This is actually slower than the other one...
    # No idea if it works
    word_scores = {}
    i = 0
    for guess_word in words:
        i += 1
        start_time = time.time()

        word_scores[guess_word] = 0
        pattern_occurrences = []
        for answer_word in words:
            key = wordle_compare(guess_word, answer_word) # tuple of gls, yls, dls

            found = False
            for pattern in pattern_occurrences:
                if pattern[0] == key:
                    pattern[1] += 1/len(words)
                    found = True
                    break
            if not found:
                pattern_occurrences.append([key, 1/len(words)])

        for pattern in pattern_occurrences:
            gls, yls, dls = pattern[0]
            valid_word_count = 0
            for possible_valid_word in words:
                valid_word_count += is_good_word(possible_valid_word, gls, yls, dls)[0]
            
            try:
                word_scores[guess_word] += pattern[1] * -math.log(valid_word_count / len(words), 2)
            except:
                pass

        time_taken = time.time() - start_time
        print(
            "%i/%i: %.2f \t %s \t %.2f \t %.2f"
            % (
                i,
                len(words),
                i / len(words) * 100,
                guess_word,
                word_scores[guess_word],
                time_taken,
            )
        )

    # THIS BLOCK OF CODE IS ABOUT THE SAME SPEED
    # BUT IT CAN BE SPEED UP BY HALFING THE TABLE
    # BUT IT STILL WOULD BE REALLY SLOW
    # AND IT WOULD NEVER "WORK BETTER" THAN THE ABOVE
    """
    word_table = {}
    for guess_word in words:
        for answer_word in words:
            word_table[guess_word + answer_word] = wordle_compare(guess_word, answer_word)

    word_scores = {}
    i = 0
    for key in word_table:
        i += 1
        guess_word = key[:len(key)//2]
        word_scores[guess_word] = len(words)
        for possible_valid_word in words:
            gls, yls, dls = word_table[key]
            word_scores[guess_word] -= is_good_word(possible_valid_word, gls, yls, dls)[0]

        print("%i/%i: %.5f \t %s \t %i" % (i, len(word_table), i/len(word_table) * 100, guess_word, word_scores[guess_word]))
    """

    ws_lst = sorted(word_scores.items(), key=lambda x: x[1], reverse=True) # Sort by highest score = [0]
    for i in range(len(ws_lst) - 1, -1, -1):
        print("%i) %s \t %0.3f" % (i + 1, ws_lst[i][0], ws_lst[i][1]))

    print("DONE IN %.3f\n" % (time.time() - t0))

    return word_scores


def main():
    print("\nPROGRAM STARTING...\n")
    bold_text("Welcome to the wordle helper!")

    print("\n")
    word_len = input_word_len()
    print("\n")
    words = get_words()
    # words = words[: int(len(words) / 5)]
    print("\n")
    double_letters = input_yes_or_no("Could there be double letters [Y/n]? ")

    words = filter_words(words, word_len, double_letters)

    print("\n")
    want_best_word = input_yes_or_no(
        "Would you like to know the best starting word [Y/n]? "
    )
    if want_best_word:
        word_scores = calc_best_words(words)
        # print(word_table)
        # bold_text("Best starting word: %s" % word_scores[list(word_scores)[0]])

    # gls = []
    # yls = []
    # dls = []

    # running = True
    # while running:
    #     run(words, gls, yls, dls)
    #     print("\n")
    #     running = input_yes_or_no("Run again [Y/n]? ")

    print("\nPROGRAM EXITING...\n")


main()
