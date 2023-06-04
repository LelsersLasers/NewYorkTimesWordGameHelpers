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

        /*
            aback drama
            green - a: 2
            ab_ck dr_ma

            if (ab_ck[0] = a) in dr_ma
                a -> !1

            yellow - a: !1


            grey - b, c, k

        */

        // YELLOWS
        for guess_letter in guess_letters_left.clone() {
            let mut positions = Vec::with_capacity(guess_letters_left.len());
            for answer_letter in &answer_letters_left {
                if &guess_letter == answer_letter {
                    let mut pos = None;
                    for (index, letter) in guess_letters.iter().enumerate() {
                        if letter == answer_letter {
                            if positions.iter().any(|&p| p == index) {
                                continue;
                            }
                            pos = Some(index);
                            break;
                        }
                    }
                    if let Some(pos) = pos {
                        positions.push(pos);
                    }
                }
            }

            if !positions.is_empty() {
                let pos = guess_letters_left
                    .iter()
                    .position(|letter| letter == &guess_letter)
                    .unwrap();
                guess_letters_left.remove(pos);

                positions.shrink_to_fit();
                yellow_letters.push(YellowLetter::new(guess_letter, positions));
            }
        }

        // for guess_letter in guess_letters_left.clone() {
        //     // if yellow_letters
        //     //     .iter()
        //     //     .any(|yellow_letter| yellow_letter.letter == guess_letter)
        //     // {
        //     //     let pos = guess_letters_left
        //     //         .iter()
        //     //         .position(|letter| letter == &guess_letter)
        //     //         .unwrap();
        //     //     guess_letters_left.remove(pos);
        //     //     continue;
        //     // }
        //     // let mut positions = Vec::new();
        //     let mut positions = Vec::with_capacity(guess_letters_left.len());
        //     for answer_letter in &answer_letters_left {
        //         if &guess_letter == answer_letter {
        //             let mut pos = None;
        //             for (index, letter) in guess_letters.iter().enumerate() {
        //                 if letter == answer_letter {
        //                     if positions.iter().any(|&p| p == index) {
        //                         continue;
        //                     }
        //                     pos = Some(index);
        //                 }
        //             }
        //             if let Some(pos) = pos {
        //                 positions.push(pos);
        //             }
        //         }
        //     }

        //     if !positions.is_empty() {
        //         let pos = guess_letters_left
        //             .iter()
        //             .position(|letter| letter == &guess_letter)
        //             .unwrap();
        //         guess_letters_left.remove(pos);

        //         positions.shrink_to_fit();
        //         yellow_letters.push(YellowLetter::new(guess_letter, positions));
        //     }
        // }

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
            for pos in &yellow_letter.positions {
                if letter_list[*pos] == yellow_letter.letter {
                    return false;
                }
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
    positions: Vec<usize>,
}
impl YellowLetter {
    pub fn new(letter: char, positions: Vec<usize>) -> Self {
        Self { letter, positions }
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
