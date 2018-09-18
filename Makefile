build:
	python setup.py clean --all sdist bdist_wheel

clean:
	rm -rf build
	rm -rf dist
	rm -rf htmlcov

publish: clean build
	twine upload --skip-existing dist/* -r pypi
