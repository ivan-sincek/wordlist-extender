# Wordlist Extender

Extend wordlist by appending digits and special characters to each word.

Check an already existing wordlist [here](https://github.com/ivan-sincek/wordlist-extender/blob/main/dict/wordlist.txt) and the extended wordlist [here](https://github.com/ivan-sincek/wordlist-extender/blob/main/dict/extended_wordlist_capitalize_d3_c1_min8.txt).

**Please be careful not to crash your PC by using a too large wordlist or extending too far.**

Feel free to tweak this tool to your liking.

Tested on Kali Linux v2023.1 (64-bit).

Made for educational purposes. I hope it will help!

## How to Run

Open your preferred console from [/src/](https://github.com/ivan-sincek/wordlist-extender/tree/main/src) and run the commands shown below.

Run the script:

```fundamental
python3 wordlist_extender.py
```

If a strong password policy is enforced, passwords usually start with one capitalized word followed by a few digits and one special character at the end (e.g. Password123!).

What I use most of the time:

```fundamental
python3 wordlist_extender.py -w wordlist.txt -t capitalize -d 3 -c 1 -min 8
```

## Runtime

```fundamental
┌──(root💀kali)-[~/Desktop]
└─# python3 wordlist_extender.py -w wordlist.txt -t capitalize -d 3 -c 1 -min 8
############################################################################
#                                                                          #
#                          Wordlist Extender v4.0                          #
#                                       by Ivan Sincek                     #
#                                                                          #
# Extend wordlist by appending digits and special characters to each word. #
# GitHub repository at github.com/ivan-sincek/wordlist-extender.           #
#                                                                          #
############################################################################
[?] Reading 'wordlist.txt' and preparing words...
[+] Total start words: 1
[?] Transforming the words...
[?] Extending the words...
[?] Removing the short/long words...
[+] Total end words: 18000
[?] Writing the extended wordlist to a file...
[+] Extended wordlist has been saved to 'extended_wordlist_capitalize_d3_c1_min8.txt'
```

## Usage

```fundamental
Wordlist Extender v4.0 ( github.com/ivan-sincek/wordlist-extender )

Usage:   python3 wordlist_extender.py -w wordlist     [-t transform ] [-d digits] [-c characters] [-min minimum]
Example: python3 wordlist_extender.py -w wordlist.txt [-t capitalize] [-d 3     ] [-c 1         ] [-min 8      ]

DESCRIPTION
    Extend wordlist by appending digits and special characters to each word
    Special characters come after digits
    Example: password -> Password123!
WORDLIST
    Wordlist to extend
    Spacing will be stripped, empty lines ignored, and duplicates removed
    -w <wordlist> - wordlist.txt | etc.
TRANSFORM
    Transform words
    -t <transform> - capitalize | lowercase | uppercase | all
DIGITS
    Number of digits to append
    -digits <digits> - 1 | 2 | 3 | etc.
CHARACTERS
    Number of special characters to append
    -c <characters> - 1 | 2 | 3 | etc.
MINIMUM
    Minimum length of extended words
    -min <minimum> - 8 | etc.
MAXIMUM
    Maximum length of extended words
    -max <maximum> - 8 | etc.
SORT
    Sort the extended wordlist by word length
    -s <sort> - asc | desc
```
