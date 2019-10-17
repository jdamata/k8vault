.DEFAULT_GOAL := build
.PHONY: build tag push test

name = k8s-vault
version = `head -1 Version`
tag = ${name}:${version}

build:
		pip install --editable .

install:
		python setup.py bdist_wheel
		python -m pip install dist/*

tag:
		git tag ${version}
		git push origin ${version}

push:
		python -m twine upload dist/*

test:
		@echo "Can't fail unit tests, if we never write them!!"
