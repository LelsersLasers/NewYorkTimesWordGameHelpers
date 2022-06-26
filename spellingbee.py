import allWords


ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


def bold_text(txt):
    print("#" * (len(txt) + 4))
    print("# " + txt + " #")
    print("#" * (len(txt) + 4))


def get_words():
    use_all = input_yes_or_no("Use more than just common words [Y/n]? ")
    if use_all:
        return allWords.get_all_words()
    return allWords.get_common_words()


def get_file_path():
    print("Enter a file path to save the outputted words to.")
    print("The file does not have to exist, and it should likely end with '.txt'.")
    try:
        user_input = input("File path (leave blank for default): ")
        assert len(user_input) > 0
        return user_input
    except:
        return "spelling_bee_output.txt"
    

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
    print("\n")
    output_path = get_file_path()

    print("\nSEARCHING...")
    good_words = calc_possible_words(words, yl, gls)
    print("FINISHED SEARCHING...\n")

    if len(good_words) > 0:
        out_str = "\n".join(good_words)
        with open(output_path, "w") as out_file:
            out_file.write(out_str)

        bold_text("%i words found:" % len(good_words))
        for i in range(len(good_words)):
            print("%i) %s" % (i + 1, good_words[i]))
    else:
        print("No words found. Did you mis-type or incorrectly enter information?")

    print("\nPROGRAM EXITING...\n")


main()
