# New York Times Word Game Helpers

CLI tools that helps you solve the word games on [The New York Times website](https://www.nytimes.com/crosswords)!

## Wordle

This tool works with [The New York Times offical Wordle](https://www.nytimes.com/games/wordle/index.html) but many other wordles as well such as [this one](http://64.98.192.13:8000/wordle/).
It works with any size wordle, as long as the standard rules for the game apply (like how the yellow, green, etc, letters are scored).

There are two versions of the tool available:
1) wordle.py - this one is very good and quick, but sometimes it will over prioritize getting the correct word rather than guaranteeing that it will get the word within 6 guesses
2) wordle2.py - this might not work at all, and takes like 2 decades to run. It tries to maximize the entropy of a guess, but the end game strat is kinda bad

Example of using  the tool to solve the offical Wordle in 2 guesses for 5/25/22:
![Helper Tool for 5/25/22](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/solving_5_26_22_wordle.PNG)

A more "reasonable" example of the tool solving offical Wordle in 4 guesses for 5/28/22:
![Helper Tool for 5/28/22](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/solving_5_28_22_wordle.PNG)

The tool works on any site that uses the normal Wordle rules for the green/yellow/dark letters (site: <http://64.98.192.41:8000/wordle/>)
![Helper Tool for other sites](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/works_on_other_sites.PNG)

It also works on any sized wordle (site: <http://64.98.192.41:8000/wordle/>)
![Helper Tool with different sizes](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/works_with_different_sizes.PNG)

## `wordle_solver`

Multithreaded brute-force Rust implementation that looks for the best starting word.
It is fairly slow and it runs in O(n^3) time.
It has no end game strat and only works for the the first word.
Successor to `wordle2.py`.

### `wordle_solver` output

```
Top 20 best starting words based on the common words
Worst to best, ranked based on expected bits of information

riles - 6.03
hares - 6.04
teals - 6.05
roles - 6.06
rites - 6.07
mares - 6.08
races - 6.08
reals - 6.09
lanes - 6.11
soare - 6.11
saner - 6.12
pares - 6.15
dares - 6.17
tires - 6.18
tries - 6.19
tears - 6.19
cares - 6.20
tales - 6.21
rates - 6.28
tares - 6.38

Top 20 best starting words based on all the words
Worst to best, ranked based on expected bits of information
riles - 5.91
rites - 5.92
treas - 5.92
aloes - 5.94
slate - 5.94
lanes - 5.95
roles - 5.96
pares - 5.97
teals - 5.99
cares - 5.99
saner - 5.99
dares - 5.99
tries - 6.00
soare - 6.01
reals - 6.01
tires - 6.02
tears - 6.06
tales - 6.10
rates - 6.12
tares - 6.21
```

## Spelling Bee

This tool works with [The New York Times offical Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) or any games that use similar rules for guessing words.
To run: simply run spellingbee.py!

Note: no screenshots because to fully solve a daily spelling bee you need to subscribe to the New York Times.
