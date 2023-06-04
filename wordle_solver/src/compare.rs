use crate::words;

#[derive(Debug)]
pub struct CompareResult {
    green_letters: Vec<GreenLetter>,
    yellow_letters: Vec<YellowLetter>,
    grey_letters: Vec<GreyLetter>,
}
impl CompareResult {
    pub fn from_compare(guess: &words::Word, answer: &words::Word) -> Self {
        let mut green_letters = Vec::with_capacity(guess.length);
        let mut yellow_letters: Vec<YellowLetter> = Vec::with_capacity(guess.length);
        let mut grey_letters = Vec::with_capacity(guess.length);

        let guess_letters = guess.word.chars().collect::<Vec<char>>();
        let answer_letters = answer.word.chars().collect::<Vec<char>>();

        let mut guess_letters_left = guess_letters.clone();
        let mut answer_letters_left = answer_letters.clone();

        // GREENS
        for ((index, guess_letter), answer_letter) in
            guess_letters.iter().enumerate().zip(answer_letters.iter())
        {
            if guess_letter == answer_letter {
                green_letters.push(GreenLetter::new(*guess_letter, index));

                let pos = guess_letters_left
                    .iter()
                    .position(|letter| letter == guess_letter)
                    .unwrap();
                guess_letters_left.remove(pos);

                let pos = answer_letters_left
                    .iter()
                    .position(|letter| letter == answer_letter)
                    .unwrap();
                answer_letters_left.remove(pos);
            }
        }

        // YELLOWS
        for guess_letter in guess_letters_left.clone() {
            if yellow_letters
                .iter()
                .any(|yellow_letter| yellow_letter.letter == guess_letter)
            {
                continue;
            }
            for answer_letter in &answer_letters_left {
                if &guess_letter == answer_letter {
                    let maybe_pos = guess_letters
                        .iter()
                        .enumerate()
                        .position(|(index, letter)| {
                            letter == &guess_letter
                                && !yellow_letters.iter().any(|yellow_letter| {
                                    yellow_letter.letter == guess_letter
                                        && yellow_letter.position == index
                                })
                                && !green_letters.iter().any(|green_letter| {
                                    green_letter.letter == guess_letter
                                        && green_letter.position == index
                                })
                        });
                    if let Some(pos) = maybe_pos {
                        yellow_letters.push(YellowLetter::new(guess_letter, pos));

                        let pos = guess_letters_left
                            .iter()
                            .position(|letter| letter == &guess_letter)
                            .unwrap();
                        guess_letters_left.remove(pos);
                    }
                }
            }
        }

        // GREYS
        for guess_letter in guess_letters_left {
            grey_letters.push(GreyLetter::new(guess_letter));
        }

        green_letters.shrink_to_fit();
        yellow_letters.shrink_to_fit();
        grey_letters.shrink_to_fit();

        Self {
            green_letters,
            yellow_letters,
            grey_letters,
        }
    }
    pub fn word_is_valid(&self, word: &words::Word) -> bool {
        // TODO!
        let letter_list = word.word.chars().collect::<Vec<char>>();
        let mut letter_list_left = letter_list.clone();

        // green letter is in the word and in the posistion
        for green_letter in &self.green_letters {
            if letter_list[green_letter.position] == green_letter.letter {
                let pos = letter_list_left
                    .iter()
                    .position(|letter| letter == &green_letter.letter);
                if let Some(pos) = pos {
                    letter_list_left.remove(pos);
                } else {
                    return false;
                }
            } else {
                return false;
            }
        }

        // yellow letter is in the word but not in the positions
        for yellow_letter in &self.yellow_letters {
            if !letter_list_left.contains(&yellow_letter.letter) {
                return false;
            }
            if letter_list[yellow_letter.position] == yellow_letter.letter {
                return false;
            }
            let pos = letter_list_left
                .iter()
                .position(|letter| letter == &yellow_letter.letter)
                .unwrap();
            letter_list_left.remove(pos);
        }

        // grey letter is not in the word
        for grey_letter in &self.grey_letters {
            if letter_list_left.contains(&grey_letter.letter) {
                return false;
            }
        }

        true
    }
}

#[derive(Debug)]
pub struct GreenLetter {
    letter: char,
    position: usize,
}
impl GreenLetter {
    pub fn new(letter: char, position: usize) -> Self {
        Self { letter, position }
    }
}
#[derive(Debug)]
pub struct YellowLetter {
    letter: char,
    position: usize,
}
impl YellowLetter {
    pub fn new(letter: char, position: usize) -> Self {
        Self { letter, position }
    }
}
#[derive(Debug)]
pub struct GreyLetter {
    letter: char,
}
impl GreyLetter {
    pub fn new(letter: char) -> Self {
        Self { letter }
    }
}
