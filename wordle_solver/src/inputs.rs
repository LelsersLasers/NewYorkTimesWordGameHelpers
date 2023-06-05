use std::io::{self, Write};

pub enum WordList {
    All { length: usize },
    Common { length: usize},
    Wordle, // always 5 letters
}
impl WordList {
    pub fn file(&self) -> &str {
        match self {
            Self::All { .. } => "words/common_words.txt",
            Self::Common { .. } => "words/common_words.txt",
            Self::Wordle => "words/wordle_words.txt",
        }
    }
}

fn word_len_recusive() -> usize {
    print!("Length: ");
    io::stdout().flush().unwrap();

    let mut word_len_input = String::new();
    std::io::stdin()
        .read_line(&mut word_len_input)
        .expect("Failed to read line");

    let maybe_word_len = word_len_input.trim().parse::<usize>();
    match maybe_word_len {
        Ok(word_len) => word_len,
        Err(_) => {
            println!("Please enter a number");
            word_len_recusive()
        }
    }
}

pub fn input_word_len() -> WordList {
    println!("\nHow many letters are in the word?");
    let length = word_len_recusive();

    if length == 5 {
        let not_only_wordle = yes_or_no("\nMore than just wordle words [Y/n]? ");
        if !not_only_wordle {
            return WordList::Wordle;
        }
    }

    let only_common = yes_or_no("\nOnly common words [Y/n]? ");

    if only_common {
        WordList::Common { length }
    } else {
        WordList::All { length }
    }
}

pub fn input_duplicate_letters() -> bool {
    yes_or_no("\nCould there be double letters [Y/n]? ")
}

fn yes_or_no(prompt: &str) -> bool {
    print!("{}", prompt);
    io::stdout().flush().unwrap();

    let mut input = String::new();
    std::io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    let first_letter = input.trim().to_lowercase().chars().next().unwrap_or('y');
    first_letter != 'n'
}