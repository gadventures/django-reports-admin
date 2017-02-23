help:
	@echo "test - run tests quickly with the default Python"


test:
	pytest --ds=tests.testapp.settings -v
