import allWords


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


def get_words():
    use_all = input_yes_or_no("Use more than just common words [Y/n]? ")
    if use_all:
        return allWords.get_all_words()
    return allWords.get_common_words()


def input_yes_or_no(prompt):
    try:
        user_input = input(prompt)
        if user_input[0].lower() == "n":
            return False
    except:
        pass
    return True


def input_yellow_letter():
    print("Enter the mandatory letter (aka the 'yellow' letter).")
    while True:
        try:
            user_input = input("Mandatory Letter: ")
            letter = user_input.lower()[0]
            assert letter in ALPHABET
            return letter
        except:
            print("Enter a letter!")


def input_grey_letters():
    print("Enter the optional letters (aka the 'grey' letters).")
    letters = []
    try:
        user_input = input("Letters (ex: 'fdtale' without the ''s): ")
        letters_input = user_input.lower()
        for letter in letters_input:
            assert letter in ALPHABET
            letters.append(letter)
        return letters
    except:
        print("Hint: you are doing something wrong (enter only letters)")


def is_good_word(word, yl, gls):

    if len(word) < 4:
        return False

    letter_lst = list(word)

    if yl not in word:
        return False
    letter_lst.remove(yl)
    for gl in gls:
        while gl in letter_lst:
            letter_lst.remove(gl)
    return len(letter_lst) == 0


def calc_possible_words(words, yl, gls):
    good_words = []
    for word in words:
        if is_good_word(word, yl, gls):
            good_words.append(word)
    return good_words


def main():
    print("\nPROGRAM STARTING...\n")
    bold_text("Welcome to the Spelling Bee helper!")

    print("\n")
    words = get_words()

    print("\nENTER INFORMATION...\n")

    yl = input_yellow_letter()
    print("\n")
    gls = input_grey_letters()

    print("\nSEARCHING...")
    good_words = calc_possible_words(words, yl, gls)
    print("FINISHED SEARCHING...\n")

    if len(good_words) > 0:
        bold_text("Words:")
        for i in range(len(good_words) - 1, -1, -1):
            print("%i) %s" % (i + 1, good_words[i]))
    else:
        print("No words found. Did you mis-type or incorrectly enter information?")

    print("\nPROGRAM EXITING...\n")


main()
