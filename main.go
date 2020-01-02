package main

import (
	cmd "github.com/jdamata/k8vault/cmd"
)

var version = "dev"

func main() {
	cmd.Execute(version)
}
