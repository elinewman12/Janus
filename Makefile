coverage: # Run tests with coverage
	coverage erase
	coverage run -m pytest -ra
	coverage report -m --omit='/usr/local/lib/python3.9/*'

deps: # Install dependecies
	pip3 install requirements.txt

tests: # Run tests
	pytest -ra
