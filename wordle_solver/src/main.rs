mod compare;
mod inputs;
mod words;

use std::time::Instant;

use rayon::prelude::*;

fn best_word(words: &[words::Word]) -> words::Word {
    println!("Calculating best word...\n");

    let start = Instant::now();

    let word_count = words.len();
    let i = std::sync::atomic::AtomicUsize::new(0);

    let mut word_scores = words
        .par_iter()
        // .iter()
        .map(|guess_word| {
            let mut score = 0.0;
            for answer_word in words {
                let compared = compare::CompareResult::from_compare(guess_word, answer_word);

                let mut eleminated = 0;
                for check_word in words {
                    let valid = compared.word_is_valid(check_word);
                    if !valid {
                        eleminated += 1;
                    }
                }

                // I = -log2(p)
                // want eleminates to be bigger -> p to be smaller -> I to be bigger
                let eleminated_percent = eleminated as f32 / word_count as f32;
                let p = 1.0 - eleminated_percent;
                let bits = -p.log2();

                if bits.is_infinite() {
                    println!(
                        "{} {} {} {} {} {} {:?}",
                        eleminated,
                        word_count,
                        p,
                        bits,
                        guess_word.word,
                        answer_word.word,
                        compared
                    );
                    panic!("bits is infinite")
                }

                score += bits / word_count as f32;
            }

            let word_score = words::WordScore::new(guess_word.clone(), score);

            let val = i.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            println!(
                "{} / {} ({:.2}%) : {}",
                val,
                word_count,
                (val as f32 / word_count as f32) * 100.0,
                word_score
            );
            word_score
        })
        .collect::<Vec<words::WordScore>>();

    // higher score = first
    word_scores.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());

    let duration = start.elapsed();

    println!("DONE!");
    println!("\n\nTime elapsed: {} secs\n", duration.as_secs());

    println!("Best words:");
    for word_score in word_scores.iter().take(20.min(word_count)).rev() {
        println!("{}", word_score);
    }

    let best_word = word_scores.first().unwrap();

    best_word.word.clone()
}

fn main() {
    println!("\nPROGRAM STARTING...\n");

    let words = {
        let word_len = inputs::input_word_len();
        let duplicate_letters = inputs::input_duplicate_letters();

        // let all_words = words::Word::from_file("words/all_words.txt");
        // let all_words = words::Word::from_file("words/common_words.txt");
        let all_words = words::Word::from_file("words/wordle_words.txt");
        all_words
            .into_iter()
            .filter(|word| word.is_valid(word_len, duplicate_letters))
            .collect::<Vec<words::Word>>()
    };
    let _best_word = best_word(&words);

    // let guess_word = words::Word {
    //     word: "speed".to_string(),
    //     length: 5,
    //     duplicate_letters: true,
    // };
    // let answer_word = words::Word {
    //     word: "crepe".to_string(),
    //     length: 5,
    //     duplicate_letters: true,
    // };
    // let compared = compare::CompareResult::from_compare(&guess_word, &answer_word);
    // println!("{:?}", compared);

    // let valid = compared.word_is_valid(&answer_word);
    // println!("VALID: {}", valid);
}
