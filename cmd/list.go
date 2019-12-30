package cmd

import (
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List kubeconfigs in the keychain",
	Run:   listKubeconfig,
}

func listKubeconfig(cmd *cobra.Command, args []string) {
	ring := openRing("k8vault")
	keys, err := ring.Keys()
	if err != nil {
		log.Fatal(err)
	}
	log.Info(keys)
}

func init() {
	rootCmd.AddCommand(listCmd)
}
