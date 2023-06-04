#[derive(Debug, Clone)]
pub struct Word {
    pub word: String,
    pub length: usize,
    pub duplicate_letters: bool,
}
impl Word {
    fn new(word: String) -> Word {
        let length = word.len();

        let mut duplicate_letters = false;
        let mut letters = Vec::with_capacity(length);
        for letter in word.chars() {
            if letters.contains(&letter) {
                duplicate_letters = true;
                break;
            }
            letters.push(letter);
        }

        Word {
            word,
            length,
            duplicate_letters,
        }
    }
    pub fn from_file(file_name: &str) -> Vec<Word> {
        let mut words = Vec::new();
        let file = std::fs::read_to_string(file_name).expect("Failed to read file");
        for line in file.lines() {
            let line_str = line.to_string();
            if !line_is_alphabetic(&line_str) {
                continue;
            }
            let word = Word::new(line_str);
            words.push(word);
        }
        words
    }
    pub fn is_valid(&self, length: usize, duplicate_letters: bool) -> bool {
        self.length == length && (duplicate_letters || !self.duplicate_letters)
    }
}

#[derive(Debug)]
pub struct WordScore {
    pub word: Word,
    pub score: u32,
}
impl WordScore {
    pub fn new(word: Word, score: u32) -> WordScore {
        WordScore { word, score }
    }
}

fn line_is_alphabetic(line: &str) -> bool {
    for letter in line.chars() {
        if !letter.is_alphabetic() {
            return false;
        }
    }
    true
}
