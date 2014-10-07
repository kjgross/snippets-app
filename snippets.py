# This script reads and writes to csv files.
# Given a name or a snippet, it can find and print out that particular row.
# Given a name and a snippet, it can write a new row
# Given a snippet, it can search for the existing row to update it or append a change to the end.

## QUESTIONS:
#1. How do I make my update a replace instead of an append? DONE! Compare Update to Update2

import logging
import csv
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="output.log", level=logging.DEBUG)


def put(name, snippet, filename):
	"""Store a snippet with an associated name in the CSV file"""
	logging.info("writing {}:{} to {}".format(name, snippet, filename))
	logging.debug("Opening file")
	with open(filename, "a") as f:
		writer = csv.writer(f)
		logging.debug("Writing snippet to file")
		writer.writerow([name,snippet])
	logging.debug("Write successful")
	return name, snippet


def get(name, filename):
	"""read the line for a given name in a file"""
	logging.info("Reading {} from {}".format(name, filename))
	logging.debug("Opening file")
	with open(filename, "r+") as f:
		reader = csv.reader(f)
		logging.debug("Reading name/snippet from file")
		in_file = False
		for row in reader:
			if str(row[0]) == name:
				in_file = True
				print row
		if in_file == False:
			print "That's not in this file"
	logging.debug("Read successful")
	return name, filename

def search(snippet_portion, filename):
	"""Add a search command that looks through your snippets and 
	find the ones containing a certain string."""
	logging.info("Searching for {} in {}".format(snippet_portion, filename))
	logging.debug("Opening file")
	with open(filename, "r+") as f:
		reader = csv.reader(f)
		logging.debug("Searching for")
		in_file = False
		for row in reader:
			if str(row[1]) == snippet_portion:
				in_file = True
				print row
		if in_file == False:
			print "That's not in this file"
	logging.debug("Search complete")
	return snippet_portion, filename	

def update(snippet_original, filename):
## THIS IS APPENDING, NOT REPLACING 
	""" Find a snippet, then allow user to change the snippet to something new"""
	logging.info("Searching for {} in {}".format(snippet_original, filename))
	logging.debug("Opening file")
	with open(filename, "r+") as f:
		reader = csv.reader(f)
		writer = csv.writer(f)
		logging.debug("Searching for '{}'".format(snippet_original))
		in_file = False
		for row in reader:
			if str(row[1]) == snippet_original:
				in_file = True
				print row
				new_text = raw_input("Insert new snippet text: ")
				row = writer.writerow([str(row[0]), new_text])
				print row
		if in_file == False:
			print "That's not in this file"
	logging.debug("Search complete")
	return snippet_original, filename	

def update2(snippet_original, filename, change):
## THIS REPLACES, NOT APPENDS
	"""Read in the file to a dictionary, make any changes, spit out new stuff from memory"""
	logging.info("Reading {} from {}".format(snippet_original, filename))
	logging.debug("Opening file")
	with open(filename, "r+") as f:
		reader = csv.reader(f)
		logging.debug("Reading name/snippet from file")
		in_file = False
		mydict = {}
		for row in reader:
			if snippet_original != str(row[1]):
				mydict.update({row[0]: row[1]})
			else:
				mydict.update({row[0]: change})
		print mydict.keys()
	with open(filename, "w") as f:
		writer = csv.writer(f)
		for key in mydict:
			writer.writerow([str(key),str(mydict[key])])
	logging.debug("Read successful")
	return snippet_original, filename
		


def make_parser():
	"""Construct the command line parser """
	logging.info("Constructing parser")
	description = "Store and retrieve snippets of text"
	parser = argparse.ArgumentParser(description = description)

	subparsers = parser.add_subparsers(dest="command", help="Available commands")

	# Subparser for the put command
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help = "Store a snippet")
	put_parser.add_argument("name", help="The name of the snippet")
	put_parser.add_argument("snippet", help="The snippet")
	put_parser.add_argument("filename", default="snippets.csv", nargs="?", help="The snippet filename")
	
	# Subparser for the get command
	logging.debug("Constructing get subparser")
	get_parser = subparsers.add_parser("get", help="Get a snippet")
	get_parser.add_argument("name", help="The name of the snippet")
	get_parser.add_argument("filename", default="snippets.csv", nargs="?", 
		help="The Snippet filename")

	# Subparser for the search command
	logging.debug("Constructing search subparser")
	search_parser = subparsers.add_parser("search", help="Search for a snippet")
	search_parser.add_argument("snippet_portion", help="The snippet you're searching for")
	search_parser.add_argument("filename", default="snippets.csv", nargs="?", 
		help="The Snippet filename")

	# Subparser for the update command
	logging.debug("Constructing update subparser")
	update_parser = subparsers.add_parser("update", help="Search for a snippet")
	update_parser.add_argument("snippet_original", help="The snippet you're searching for")
	update_parser.add_argument("filename", default="snippets.csv", nargs="?", 
		help="The Snippet filename")

	# Subparser for the update2 command
	logging.debug("Constructing update2 subparser")
	update2_parser = subparsers.add_parser("update2", help="Search for a snippet")
	update2_parser.add_argument("snippet_original", help="The snippet you're searching for")
	update2_parser.add_argument("filename", default="snippets.csv", nargs="?", 
		help="The Snippet filename")
	update2_parser.add_argument("change", help="The snippet you want to change it to")

	return parser




def main():
	""" Main function """
	logging.info("Starting snippets")
	parser = make_parser()
	arguments = parser.parse_args(sys.argv[1:])
	
	# Convert parsed arguments from Namespace to dictionary
	arguments = vars(arguments)
	command = arguments.pop("command")

	if command == "put":
		name, snippet = put(**arguments)
		print "Stored '{}' as '{}'".format(snippet, name)
	elif command == "get":
		name, filename = get(**arguments)
		print "reading '{}' from '{}'".format(name,filename)
	elif command == "search":
		snippet_portion, filename = search(**arguments)
		print "Searching for '{}' in '{}'".format(snippet_portion,filename)
	elif command == "update":
		snippet_original, filename = update(**arguments)
		print "Searching for '{}' in '{}', then updating".format(snippet_original, filename)
	elif command == "update2":
		snippet_original, filename = update2(**arguments)
		print "update2 for '{}'' in '{}'".format(snippet_original, filename)


if __name__ == "__main__":
	main()




