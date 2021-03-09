# Wordlist Extender

Extend wordlist by appending digits and special characters to each word.

Check an already existing wordlist [here](https://github.com/ivan-sincek/wordlist-extender/blob/main/dict/wordlist.txt) and the extended wordlist [here](https://github.com/ivan-sincek/wordlist-extender/blob/main/dict/extended_wordlist.txt).

Feel free to tweak this tool to your liking.

Tested on Kali Linux v2020.3 (64-bit).

Made for educational purposes. I hope it will help!

## How to Run

Open your preferred console from [/src/](https://github.com/ivan-sincek/wordlist-extender/tree/main/src) and run the commands shown below.

Run the script:

```fundamental
python3 wordlist_extender.py
```

If strong password policy is enforced, passwords usually start with one capitalized word followed by few digits and one special character at the end (e.g. Password123!).

What I use all the time:

```fundamental
python3 wordlist_extender.py -f wordlist.txt -d 3 -c 1 -t capitalize -min 8
```

## Images

<p align="center"><img src="https://github.com/ivan-sincek/wordlist-extender/blob/main/img/help.jpg" alt="Help"></p>

<p align="center">Figure 1 - Help</p>

<p align="center"><img src="https://github.com/ivan-sincek/wordlist-extender/blob/main/img/extending.jpg" alt="Extending"></p>

<p align="center">Figure 2 - Extending</p>
