export GO111MODULE=on
VERSION=$(shell git describe --tags --candidates=1 --dirty)
BUILD_FLAGS=-ldflags="-X main.version=$(VERSION)"
# CERT_ID ?= TODO
SRC=$(shell find . -name '*.go')

.PHONY: all clean release install

all: k8vault-linux-amd64 k8vault-darwin-amd64

clean:
	rm -f k8vault k8vault-linux-amd64 k8vault-darwin-amd64

k8vault-linux-amd64: $(SRC)
	GOOS=linux GOARCH=amd64 go build $(BUILD_FLAGS) -o $@ .

k8vault-darwin-amd64: $(SRC)
	GOOS=darwin GOARCH=amd64 go build $(BUILD_FLAGS) -o $@ .

install:
	rm -f k8vault
	go build $(BUILD_FLAGS) .
	# codesign --options runtime --timestamp --sign "$(CERT_ID)" k8vault
	mv k8vault ~/bin/
