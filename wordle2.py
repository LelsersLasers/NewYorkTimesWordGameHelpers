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


def clean_word_list(words, word_len, double_letters):
    filtered_words = []
    for word in words:
        if len(word) == word_len and not (
            not double_letters and has_double_letters(word)
        ):
            filtered_words.append(word)
    return filtered_words


def get_words(word_len):
    only_common = input_yes_or_no("Only common words [Y/n]? ")
    if only_common:
        if word_len == 5:
            not_only_wordle = input_yes_or_no(
                "Use more than only offical Wordle answer words [Y/n]? "
            )
            if not not_only_wordle:
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
            return False
    for yl in yls:
        if yl[0] not in letter_lst:
            return False
        for idx in yl[1]:
            if word[idx] == yl[0]:
                return False
        letter_lst.remove(yl[0])
    for dl in dls:
        if dl in letter_lst:
            return False
    return True


def wordle_compare(answer, guess):
    # ARE THEY BACKWARDS? ONLY THINKG THT WOULD CHANGE IS THE DLS AND MAYBE WHERE THE YLS ARE NOT
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


def filter_words(words, gls, yls, dls):
    filtered_words = []
    for word in words:
        good = is_good_word(word, gls, yls, dls)
        if good:
            filtered_words.append(word)
    return filtered_words


def run(all_words, filtered_words, letter_counts, letter_weights, gls, yls, dls):
    print("\nENTER INFORMATION...\n")

    gls = input_green_letters(len(all_words[0]), gls)
    print("\n")
    yls = input_yellow_letters(len(all_words[0]))
    print("\n")
    dls = input_dark_letters("Enter letters that are not in the word.", dls)

    print("")

    filtered_words = filter_words(filtered_words, gls, yls, dls)

    if len(filtered_words) == 1:
        bold_text("The word is: %s" % filtered_words[0])
    elif len(filtered_words) > 1:
        bold_text("The answer could be one of %i words" % len(filtered_words))
        should_show = len(filtered_words) < 10 or input_yes_or_no(
            "Would you like to see those words [Y/n]? "
        )
        if should_show:
            ranked_words = rank_words(filtered_words, letter_counts, letter_weights)
            for i in range(len(ranked_words) - 1, -1, -1):
                print("%i) %s" % (i + 1, ranked_words[i][0]))
            temp = input_yes_or_no("Press enter to continue...\n")

        possible_words = calc_best_words(all_words, filtered_words, gls, yls, dls)
        bold_text("Next Guesses:")
        for i in range(len(possible_words) - 1, -1, -1):
            print("%2i) %s\t%.5f" % (i + 1, possible_words[i][0], possible_words[i][1]))
    else:
        print("No words found. Did you mis-type or incorrectly enter information?")


def rank_words(words, letter_counts, letter_weights):
    word_scores = {}
    for word in words:
        word_scores[word] = 0
        for i in range(len(word)):
            word_scores[word] += (
                letter_counts[ALPHABET.index(word[i])][0] * letter_weights["yellow"]
            )
            word_scores[word] += (
                letter_counts[ALPHABET.index(word[i])][1][i] * letter_weights["green"]
            )
        if has_double_letters(word):
            word_scores[word] *= letter_weights["double"]
    ranked_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_words


def calc_best_words(all_words, filtered_words, gls, yls, dls):
    print("\nSTARTING CALCULATIONS...")
    t0 = time.time()

    # THIS MIGHT WORK, BUT IT TAKES FOREVER, SO IDK IF IT WORKS
    """
    word_scores = {}
    i = 0
    for guess_word in all_words:
        i += 1
        start_time = time.time()

        word_scores[guess_word] = 0
        for answer_word in filtered_words:
            new_gls, new_yls, new_dls = wordle_compare(guess_word, answer_word)
            # new_gls += gls
            # new_yls += yls
            # new_dls += dls
            for possible_valid_word in filtered_words:
                word_scores[guess_word] += not is_good_word(possible_valid_word, new_gls, new_yls, new_dls)
        # word_scores[guess_word] = -math.log(word_scores[guess_word] / (len(all_words) * len(filtered_words)), 2) # convert to bits of information

        time_taken = time.time() - start_time
        print(
            "%i/%i: %.2f%% \t%s\tI: %.2f\t%.2f sec"
            % (
                i,
                len(all_words),
                i / len(all_words) * 100,
                guess_word,
                word_scores[guess_word],
                time_taken,
            )
        )
    """

    # I think this works
    # Its a lot faster, but still really slow
    # Uses https://www.youtube.com/watch?v=v68zYyaEmEA video's math
    word_scores = {}
    i = 0
    # oof = []
    for guess_word in all_words:
        i += 1
        start_time = time.time()

        word_scores[guess_word] = 0
        pattern_occurrences = []
        for answer_word in filtered_words:
            key = wordle_compare(guess_word, answer_word)  # tuple of gls, yls, dls

            found = False
            for pattern in pattern_occurrences:
                if pattern[0] == key:
                    pattern[1] += 1 / len(filtered_words)
                    found = True
                    break
            if not found:
                pattern_occurrences.append([key, 1 / len(filtered_words)])
        for pattern in pattern_occurrences:
            new_gls, new_yls, new_dls = pattern[0]
            # new_gls += gls
            # new_yls += yls
            # new_dls += dls
            valid_word_count = 0
            for possible_valid_word in filtered_words:
                good_word = is_good_word(possible_valid_word, new_gls, new_yls, new_dls)
                valid_word_count += good_word
                if good_word and possible_valid_word == guess_word:
                    valid_word_count -= 1
            try:
                # if valid_word_count < 1 and guess_word in filtered_words:
                #     oof.append([guess_word, valid_word_count])
                word_scores[guess_word] += pattern[1] * -math.log(
                    valid_word_count / len(filtered_words), 2
                )
            except:
                pass

        time_taken = time.time() - start_time
        print(
            "%i/%i: %.2f%% \t%s\tI: %.2f \t %.2f sec"
            % (
                i,
                len(all_words),
                i / len(all_words) * 100,
                guess_word,
                word_scores[guess_word],
                time_taken,
            )
        )

    ws_lst = sorted(
        word_scores.items(), key=lambda x: x[1], reverse=True
    )  # Sort by highest score = [0]
    ws_lst = ws_lst[:10]

    print("DONE IN %.2f seconds" % (time.time() - t0))
    print("Advanced search info:")
    print("- Total guessable words: %i" % len(all_words))
    print("- Total possible answer words words: %i" % len(filtered_words))
    print("- Total possible answer words: %i" % len(ws_lst))
    print(
        "- Information (bits) of possible answer words: %.2f\n"
        % math.log(len(filtered_words), 2)
    )

    # for o in oof:
    #     print(o)

    return ws_lst


def calc_double_letter_weight(words):
    double_letter_words = 0
    for word in words:
        double_letter_words += has_double_letters(word)
    return 1 - (1 - (double_letter_words / len(words)) / 2)


def calc_letter_counts(words):
    letter_counts = []
    for i in range(len(ALPHABET)):
        temp = [0] * len(words[0])
        letter_counts.append([0, temp])

    for word in words:
        for i in range(len(word)):
            letter_counts[ALPHABET.index(word[i])][0] += 1
            letter_counts[ALPHABET.index(word[i])][1][i] += 1
    return letter_counts


def main():

    letter_weights = {"yellow": 4, "green": 1, "double": -1}

    print("\nPROGRAM STARTING...\n")
    bold_text("Welcome to the wordle helper!")

    print("\n")
    word_len = input_word_len()
    print("\n")
    words = get_words(word_len)
    print("\n")
    double_letters = input_yes_or_no("Could there be double letters [Y/n]? ")

    words = clean_word_list(words, word_len, double_letters)

    if double_letters:
        letter_weights["double"] = calc_double_letter_weight(words)
    letter_counts = calc_letter_counts(words)

    print("\n")
    want_best_word = input_yes_or_no(
        "Would you like to know the best starting word [Y/n]? "
    )
    if want_best_word:
        word_scores = calc_best_words(words, words, [], [], [])
        bold_text("Best starting word: %s" % word_scores[0][0])

    gls = []
    yls = []
    dls = []
    filtered_words = words.copy()

    running = True
    while running:
        run(words, filtered_words, letter_counts, letter_weights, gls, yls, dls)
        print("\n")
        running = input_yes_or_no("Run again [Y/n]? ")

    print("\nPROGRAM EXITING...\n")


main()
