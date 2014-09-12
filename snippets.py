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
		logging.debug("Writing snippet to file".format(name, snippet))
		writer.writerow([name,snippet])
	logging.debug("Write successful")
	return name, snippet

def make_parser():
	"""Construct the comman line parser """
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

if __name__ == "__main__":
	main()


