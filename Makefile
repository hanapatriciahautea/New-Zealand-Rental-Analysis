# makes 'phony' targets -- specifies these are commands to run & not to be confused with any actual files named 'all' or 'run'
.PHONY: all run

# for convenience -- if someone's system uses Python 3 instead of Python, they only need to change this one line
PYTHON = python

# defines a target called 'all' so that if someone just uses 'make'/'make all', it will do whatever 'run' does
all: run 

# entering 'make run' automatically runs the code/main.py file
run:
	$(PYTHON) code/main.py --auto