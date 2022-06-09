# WordleHelper

CLI tool that helps you solve the Wordle easier!

To use: simply run "helper.py"!

Note:
- helper.py is very good/quick, but sometimes it will over prioritize getting the correct word rather than guaranteeing that it will get the word within 6 guesses
- helper2.py might not work at all, and takes like 2 decades to run
    - It tries to maximize the entropy of a guess, but the end game strat is kinda bad

Example of using  the tool to solve the offical Wordle in 2 guesses for 5/25/22:
![Helper Tool for 5/25/22](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/solving_5_26_22_wordle.PNG)

A more "reasonable" example of the tool solving offical Wordle in 4 guesses for 5/28/22:
![Helper Tool for 5/28/22](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/solving_5_28_22_wordle.PNG)

The tool works on any site that uses the normal Wordle rules for the green/yellow/dark letters (site: <http://64.98.192.41:8000/wordle/>)
![Helper Tool for other sites](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/works_on_other_sites.PNG)

It also works on any sized wordle (site: <http://64.98.192.41:8000/wordle/>)
![Helper Tool with different sizes](https://github.com/LelsersLasers/WordleHelper/raw/main/showcase/works_with_different_sizes.PNG)

# Todo

helper2.py
- If entropy is tried, rank the same way helper.py does
