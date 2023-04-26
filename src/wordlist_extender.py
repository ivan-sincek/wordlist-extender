#!/usr/bin/env python3

import sys
import os

# -------------------------- INFO --------------------------

def basic():
	global proceed
	proceed = False
	print("Wordlist Extender v4.0 ( github.com/ivan-sincek/wordlist-extender )")
	print("")
	print("Usage:   python3 wordlist_extender.py -w wordlist     [-t transform ] [-d digits] [-c characters] [-min minimum]")
	print("Example: python3 wordlist_extender.py -w wordlist.txt [-t capitalize] [-d 3     ] [-c 1         ] [-min 8      ]")

def advanced():
	basic()
	print("")
	print("DESCRIPTION")
	print("    Extend wordlist by appending digits and special characters to each word")
	print("    Special characters come after digits")
	print("    Example: password -> Password123!")
	print("WORDLIST")
	print("    Wordlist to extend")
	print("    Spacing will be stripped, empty lines ignored, and duplicates removed")
	print("    -w <wordlist> - wordlist.txt | etc.")
	print("TRANSFORM")
	print("    Transform words")
	print("    -t <transform> - capitalize | lowercase | uppercase | all")
	print("DIGITS")
	print("    Number of digits to append")
	print("    -digits <digits> - 1 | 2 | 3 | etc.")
	print("CHARACTERS")
	print("    Number of special characters to append")
	print("    -c <characters> - 1 | 2 | 3 | etc.")
	print("MINIMUM")
	print("    Minimum length of extended words")
	print("    -min <minimum> - 8 | etc.")
	print("MAXIMUM")
	print("    Maximum length of extended words")
	print("    -max <maximum> - 8 | etc.")
	print("SORT")
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

args = {"wordlist": None, "transform": None, "digits": None, "characters": None, "minimum": None, "maximum": None, "sort": None}

def validate(key, value):
	global args
	value = value.strip()
	if len(value) > 0:
		if key == "-w" and args["wordlist"] is None:
			args["wordlist"] = value
			if not os.path.isfile(args["wordlist"]):
				error("Wordlist does not exists")
			elif not os.access(args["wordlist"], os.R_OK):
				error("Wordlist does not have read permission")
			elif not os.stat(args["wordlist"]).st_size > 0:
				error("Wordlist is empty")
		elif key == "-t" and args["transform"] is None:
			args["transform"] = value.lower()
			if args["transform"] not in ["capitalize", "lowercase", "uppercase", "all"]:
				error("To transform words specify either 'capitalize', 'lowercase', 'uppercase', or 'all'")
		elif key == "-d" and args["digits"] is None:
			args["digits"] = value
			if not args["digits"].isdigit():
				error("Number of digits must be numeric")
			else:
				args["digits"] = int(args["digits"])
				if args["digits"] < 1:
					error("Number of digits must be greater than zero")
		elif key == "-c" and args["characters"] is None:
			args["characters"] = value
			if not args["characters"].isdigit():
				error("Number of special characters must be numeric")
			else:
				args["characters"] = int(args["characters"])
				if args["characters"] < 1:
					error("Number of special characters must be greater than zero")
		elif key == "-min" and args["minimum"] is None:
			args["minimum"] = value
			if not args["minimum"].isdigit():
				error("Minimum length of extended words must be numeric")
			else:
				args["minimum"] = int(args["minimum"])
				if args["minimum"] < 1:
					error("Minimum length of extended words must be greater than zero")
		elif key == "-max" and args["maximum"] is None:
			args["maximum"] = value
			if not args["maximum"].isdigit():
				error("Maximum length of extended words must be numeric")
			else:
				args["maximum"] = int(args["maximum"])
				if args["maximum"] < 1:
					error("Maximum length of extended words must be greater than zero")
		elif key == "-s" and args["sort"] is None:
			args["sort"] = value.lower()
			if args["sort"] not in ["asc", "desc"]:
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
elif argc % 2 == 0 and argc <= len(args) * 2:
	for i in range(1, argc, 2):
		validate(sys.argv[i], sys.argv[i + 1])
	if args["wordlist"] is None or not check(argc, args):
		error("Missing a mandatory option (-w) and/or optional (-t, -d, -c, -min, -max, -s)", True)
else:
	error("Incorrect usage", True)

# --------------------- VALIDATION END ---------------------

# ----------------------- TASK BEGIN -----------------------

def unique(sequence):
	seen = set()
	return [x for x in sequence if not (x in seen or seen.add(x))]

def read_file(file):
	tmp = []
	with open(file, "r", encoding = "ISO-8859-1") as wordlist:
		for word in wordlist:
			# strip all spacing
			word = word.strip()
			# strip only new lines
			# word = word.strip("\n")
			if word:
				tmp.append(word)
	wordlist.close()
	return unique(tmp)

def write_file(wordlist, out):
	print("[?] Writing the extended wordlist to a file...")
	with open(out, "w") as stream:
		for word in wordlist:
			stream.write(word + "\n")
	stream.close()
	print(("[+] Extended wordlist has been saved to '{0}'").format(out))

def transform_words(wordlist, transform = "all"):
	tmp = []
	if transform == "capitalize":
		for word in wordlist:
			tmp.append(word.capitalize())
	elif transform == "lowercase":
		for word in wordlist:
			tmp.append(word.lower())
	elif transform == "uppercase":
		for word in wordlist:
			tmp.append(word.upper())
	elif transform == "all":
		for word in wordlist:
			tmp.extend([word.capitalize(), word.lower(), word.upper()])
	else:
		tmp = wordlist
	return tmp

def append_char(wordlist, charset, iterations = 1):
	tmp = []
	for word in wordlist:
		for char in charset:
			tmp.append(word + char)
	iterations = iterations - 1
	if iterations > 0:
		tmp.extend(append_char(tmp, charset, iterations))
	return tmp

def remove_words(wordlist, minimum = None, maximum = None):
	tmp = []
	if minimum and not maximum:
		for word in wordlist:
			if len(word) >= minimum:
				tmp.append(word)
	elif not minimum and maximum:
		for word in wordlist:
			if len(word) <= maximum:
				tmp.append(word)
	elif minimum and maximum:
		for word in wordlist:
			length = len(word)
			if length >= minimum and length <= maximum:
				tmp.append(word)
	else:
		tmp = wordlist
	return tmp

def sort_words(wordlist, direction = "asc"):
	if direction == "asc":
		wordlist = sorted(wordlist, key = len)
	elif direction == "desc":
		wordlist = sorted(wordlist, key = len, reverse = True)
	return wordlist

def extend(wordlist, transform = None, digits = None, characters = None, minimum = None, maximum = None, sort = None):
	append = ""
	print(("[?] Reading '{0}' and preparing words...").format(wordlist))
	wordlist = read_file(wordlist)
	if not wordlist:
		print("[!] No words were found")
	else:
		print(("[+] Total start words: {0}").format(len(wordlist)))
		if transform:
			print("[?] Transforming the words...")
			wordlist = transform_words(wordlist, transform)
			wordlist = unique(wordlist)
			append = ("{0}_{1}").format(append, transform)
		if digits or characters:
			print("[?] Extending the words...")
			if digits:
				# modify the charset to your liking
				charset = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
				wordlist.extend(append_char(wordlist, charset, digits))
				wordlist = unique(wordlist)
				append = ("{0}_d{1}").format(append, digits)
			if characters:
				# modify the charset to your liking
				charset = ['!', '"', '#', '%', '&', '\'', '(', ')', '*', '+', '-', '/', '=', '?', '@', '^', '_', '$']
				wordlist.extend(append_char(wordlist, charset, characters))
				wordlist = unique(wordlist)
				append = ("{0}_c{1}").format(append, characters)
		if minimum or maximum:
			print("[?] Removing the short/long words...")
			wordlist = remove_words(wordlist, minimum, maximum)
			if minimum:
				append = ("{0}_min{1}").format(append, minimum)
			if maximum:
				append = ("{0}_max{1}").format(append, maximum)
		if not wordlist:
			print("[!] No words are left")
		else:
			print(("[+] Total end words: {0}").format(len(wordlist)))
			if sort:
				print("[?] Sorting the extended wordlist by word length...")
				wordlist = sort_words(wordlist, sort)
				append = ("{0}_{1}").format(append, sort)
			write_file(wordlist, ("extended_wordlist{0}.txt").format(append))

if proceed:
	print("############################################################################")
	print("#                                                                          #")
	print("#                          Wordlist Extender v4.0                          #")
	print("#                                       by Ivan Sincek                     #")
	print("#                                                                          #")
	print("# Extend wordlist by appending digits and special characters to each word. #")
	print("# GitHub repository at github.com/ivan-sincek/wordlist-extender.           #")
	print("#                                                                          #")
	print("############################################################################")
	extend(args["wordlist"], args["transform"], args["digits"], args["characters"], args["minimum"], args["maximum"], args["sort"])

# ------------------------ TASK END ------------------------
