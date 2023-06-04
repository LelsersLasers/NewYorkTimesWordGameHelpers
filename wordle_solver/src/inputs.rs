use std::io::{self, Write};

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

pub fn input_word_len() -> usize {
    println!("\nHow many letters are in the word?");
    word_len_recusive()
}

pub fn input_duplicate_letters() -> bool {
    print!("\nCould there be double letters [Y/n]? ");
    io::stdout().flush().unwrap();

    let mut duplicate_letters_input = String::new();
    std::io::stdin()
        .read_line(&mut duplicate_letters_input)
        .expect("Failed to read line");

    let duplicate_letters = duplicate_letters_input.trim().to_lowercase();
    duplicate_letters == "y"
}
