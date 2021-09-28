coverage: # Run tests with coverage
	coverage erase
	coverage run -m pytest -ra
	coverage report -m

deps: # Install dependecies
	pip3 install -r requirements.txt

tests: # Run tests
	pytest -ra
