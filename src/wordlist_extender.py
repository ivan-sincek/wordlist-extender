#!/usr/bin/env python3

import sys
import os

# -------------------------- INFO --------------------------

def basic():
	global proceed
	proceed = False
	print("Wordlist Extender v2.1 ( github.com/ivan-sincek/wordlist-extender )")
	print("")
	print("Usage:   python3 wordlist_extender.py -f file         -d digits -c characters -t transform")
	print("Example: python3 wordlist_extender.py -f wordlist.txt -d 3      -c 1          -t capitalize")

def advanced():
	basic()
	print("")
	print("DESCRIPTION")
	print("    Extend wordlist by appending digits and special characters to each word")
	print("    Special characters come after digits")
	print("    Example: password -> Password123!")
	print("    Feel free to tweak this tool to your liking")
	print("FILE (required)")
	print("    Specify a wordlist to extend")
	print("    Spacing will be stripped, empty lines ignored and duplicates removed")
	print("    -f <file> - wordlist.txt | etc.")
	print("DIGITS (optional)")
	print("    Specify up to how many digits to append")
	print("    -digits <digits> - 1 | 2 | 3 | etc.")
	print("CHARACTERS (optional)")
	print("    Specify up to how many special characters to append")
	print("    -c <characters> - 1 | 2 | 3 | etc.")
	print("TRANSFORM (optional)")
	print("    Transform words")
	print("    -t <transform> - capitalize | lowercase | uppercase | all")
	print("MINIMUM (optional)")
	print("    Specify a minimum length of extended words")
	print("    -min <minimum> - 8 | etc.")
	print("MAXIMUM (optional)")
	print("    Specify a maximum length of extended words")
	print("    -max <maximum> - 8 | etc.")
	print("SORT (optional)")
	print("    Sort the extended wordlist by word length")
	print("    -s <sort> - asc | desc")

# -------------------- VALIDATION BEGIN --------------------

# my own validation algorithm

proceed = True

def print_error(msg):
	print(("ERROR: {0}").format(msg))

def error(msg, help = False):
	global proceed
	proceed = False
	print_error(msg)
	if help:
		print("Use -h for basic and --help for advanced info")

args = {"file": None, "digits": None, "characters": None, "transform": None, "minimum": None, "maximum": None, "sort": None}

def validate(key, value):
	global args
	if key == "-f" and args["file"] is None:
		args["file"] = value
		if not os.path.isfile(args["file"]):
			error("File does not exists")
		elif not os.stat(args["file"]).st_size > 0:
			error("File is empty")
	elif key == "-d" and args["digits"] is None:
		args["digits"] = value
		if not args["digits"].isdigit():
			error("Number of digits must be numeric")
		elif not int(args["digits"]) > 0:
			error("Number of digits must be greater than zero")
		else:
			args["digits"] = int(args["digits"])
	elif key == "-c" and args["characters"] is None:
		args["characters"] = value
		if not args["characters"].isdigit():
			error("Number of special characters must be numeric")
		elif not int(args["characters"]) > 0:
			error("Number of special characters must be greater than zero")
		else:
			args["characters"] = int(args["characters"])
	elif key == "-t" and args["transform"] is None:
		args["transform"] = value
		if not (args["transform"] == "capitalize" or args["transform"] == "lowercase" or args["transform"] == "uppercase" or args["transform"] == "all"):
			error("To transform words specify either 'capitalize', 'lowercase', 'uppercase' or 'all'")
	elif key == "-min" and args["minimum"] is None:
		args["minimum"] = value
		if not args["minimum"].isdigit():
			error("Minimum length of extended words must be numeric")
		elif not int(args["minimum"]) > 0:
			error("Minimum length of extended words must be greater than zero")
		else:
			args["minimum"] = int(args["minimum"])
	elif key == "-max" and args["maximum"] is None:
		args["maximum"] = value
		if not args["maximum"].isdigit():
			error("Maximum length of extended words must be numeric")
		elif not int(args["maximum"]) > 0:
			error("Maximum length of extended words must be greater than zero")
		else:
			args["maximum"] = int(args["maximum"])
	elif key == "-s" and args["sort"] is None:
		args["sort"] = value
		if not (args["sort"] == "asc" or args["sort"] == "desc"):
			error("Sort order must be either 'asc' or 'desc'")

def check(argc, args):
	count = 0
	for key in args:
		if args[key] is not None:
			count += 1
	return argc - count == argc / 2

argc = len(sys.argv) - 1

if argc == 0:
	advanced()
elif argc == 1:
	if sys.argv[1] == "-h":
		basic()
	elif sys.argv[1] == "--help":
		advanced()
	else:
		error("Incorrect usage", True)
elif argc % 2 == 0 and argc <= 14:
	for i in range(1, argc, 2):
		validate(sys.argv[i], sys.argv[i + 1])
	if args["file"] == None or not check(argc, args):
		error("Missing a mandatory option (-f) and/or optional (-d, -c, -t, -min, -max, -s)", True)
else:
	error("Incorrect usage", True)

# --------------------- VALIDATION END ---------------------

# ----------------------- TASK BEGIN -----------------------

def prepare(wordlist, transform = None):
	tmp = []
	words = wordlist.split()
	for word in words:
		if transform == "capitalize":
			word = word.capitalize()
			if word not in tmp:
				tmp.append(word)
		elif transform == "lowercase":
			word = word.lower()
			if word not in tmp:
				tmp.append(word)
		elif transform == "uppercase":
			word = word.upper()
			if word not in tmp:
				tmp.append(word)
		elif transform == "all":
			word = word.capitalize()
			if word not in tmp:
				tmp.append(word)
			word = word.lower()
			if word not in tmp:
				tmp.append(word)
			word = word.upper()
			if word not in tmp:
				tmp.append(word)
		else:
			if word not in tmp:
				tmp.append(word)
	return tmp

def add_numbers(wordlist, iterations = 1):
	tmp = []
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	for word in wordlist:
		for digit in digits:
			tmp.append(word + digit)
	iterations -= 1
	if iterations > 0:
		tmp.extend(add_numbers(tmp, iterations))
	return tmp

def add_characters(wordlist, iterations = 1):
	tmp = []
	characters = ['!', '"', '#', '%', '&', '\'', '(', ')', '*', '+', '-', '/', '=', '?', '@', '^', '_', '$']
	for word in wordlist:
		for character in characters:
			tmp.append(word + character)
	iterations -= 1
	if iterations > 0:
		tmp.extend(add_characters(tmp, iterations))
	return tmp

def remove_words_min(wordlist, length = 8):
	tmp = []
	for word in wordlist:
		if len(word) >= length:
			tmp.append(word)
	return tmp

def remove_words_max(wordlist, length = 8):
	tmp = []
	for word in wordlist:
		if len(word) <= length:
			tmp.append(word)
	return tmp

def extend(file, digits = 0, characters = 0, transform = None, minimum = 0, maximum = 0, sort = None):
	suffix = ""
	print((" - Reading the '{0}'...").format(file))
	wordlist = open(file, "r").read()
	print(" - Preparing the wordlist...")
	wordlist = prepare(wordlist, transform)
	print((" - {0} words has been prepared").format(len(wordlist)))
	if transform:
		suffix = ("{0}_{1}").format(suffix, transform)
	if digits:
		print(" - Extending the wordlist with digits...")
		wordlist.extend(add_numbers(wordlist, digits))
		suffix = ("{0}_d{1}").format(suffix, digits)
	if characters:
		print(" - Extending the wordlist with special characters...")
		wordlist.extend(add_characters(wordlist, characters))
		suffix = ("{0}_c{1}").format(suffix, characters)
	if minimum:
		print(" - Removing short words...")
		wordlist = remove_words_min(wordlist, minimum)
		suffix = ("{0}_min{1}").format(suffix, minimum)
	if maximum:
		print(" - Removing long words...")
		wordlist = remove_words_max(wordlist, maximum)
		suffix = ("{0}_max{1}").format(suffix, maximum)
	if sort == "asc":
		print(" - Sorting the extended wordlist ascending by word length...")
		wordlist = sorted(wordlist, key = len)
		suffix = ("{0}_{1}").format(suffix, sort)
	elif sort == "desc":
		print(" - Sorting the extended wordlist descending by word length...")
		wordlist = sorted(wordlist, key = len, reverse = True)
		suffix = ("{0}_{1}").format(suffix, sort)
	name = ("extended_wordlist{0}.txt").format(suffix)
	with open(name, "w") as stream:
		print(" - Wirting the extended wordlist to a file...")
		for word in wordlist:
			stream.write(("{0}\n").format(word))
		print((" - Extended wordlist has been saved to '{0}'").format(name))
	stream.close()
	print((" - {0} words has been saved").format(len(wordlist)))

if proceed:
	print("############################################################################")
	print("#                                                                          #")
	print("#                          Wordlist Extender v2.2                          #")
	print("#                                       by Ivan Sincek                     #")
	print("#                                                                          #")
	print("# Extend wordlist by appending digits and special characters to each word. #")
	print("# GitHub repository at github.com/ivan-sincek/wordlist-extender.           #")
	print("# Feel free to donate bitcoin at 1BrZM6T7G9RN8vbabnfXu4M6Lpgztq6Y14.       #")
	print("#                                                                          #")
	print("############################################################################")
	extend(args["file"], args["digits"], args["characters"], args["transform"], args["minimum"], args["maximum"], args["sort"])

# ------------------------ TASK END ------------------------
