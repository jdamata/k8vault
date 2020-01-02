package cmd

import (
	"fmt"
	"io/ioutil"

	homedir "github.com/mitchellh/go-homedir"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

var getCmd = &cobra.Command{
	Use:   "get [CONFIGNAME]",
	Short: "Get a kubeconfig from the keychain",
	Args:  cobra.ExactArgs(1),
	Run:   getKubeconfig,
}

func getKubeconfig(cmd *cobra.Command, args []string) {
	ring := openRing(keychain)
	key, err := ring.Get(args[0])
	if err != nil {
		log.Fatal(err)
	}
	writeKubeconfig(key.Data)
}

func writeKubeconfig(data []byte) {
	home, err := homedir.Dir()
	if err != nil {
		log.Fatal(err)
	}
	err = ioutil.WriteFile(fmt.Sprintf("%s/.kube/config", home), data, 0640)
	if err != nil {
		log.Fatal(err)
	}
}

func init() {
	rootCmd.AddCommand(getCmd)
}
