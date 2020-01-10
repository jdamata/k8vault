package cmd

import (
	"io/ioutil"

	"github.com/99designs/keyring"
	"github.com/manifoldco/promptui"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
	"k8s.io/client-go/tools/clientcmd"
)

var addCmd = &cobra.Command{
	Use:   "add [PATH TO KUBECONFIG]",
	Short: "Add a kubeconfig to the keychain",
	Args:  cobra.ExactArgs(1),
	Run:   addKubeconfig,
}

func addKubeconfig(cmd *cobra.Command, args []string) {
	ring := openRing(keychain)
	prompt := promptui.Prompt{
		Label: "Give your kubeconfig a unique name: ",
	}
	kubeconfigName, err := prompt.Run()
	if err != nil {
		log.Fatalf("Prompt failed: %v\n", err)
	}
	if configExists(ring, kubeconfigName) {
		log.Fatal("Kubeconfig name already exists. First delete the config if you would like to update it.")
	}
	validateKubeconfig(args[0])
	data, err := ioutil.ReadFile(args[0])
	if err != nil {
		log.Fatalf("Failed to read kubeconfig from disk: %v\n", err)
	}
	err = ring.Set(keyring.Item{
		Key:  kubeconfigName,
		Data: []byte(data),
	})
	if err != nil {
		log.Fatalf("Failed to add kubeconfig to keyring: %v\n", err)
	}
}

func configExists(ring keyring.Keyring, config string) bool {
	item, _ := ring.Get(config)
	if item.Data != nil {
		return true
	}
	return false
}

func validateKubeconfig(kubeconfigPath string) {
	config := clientcmd.GetConfigFromFileOrDie(kubeconfigPath)
	err := clientcmd.Validate(*config)
	if err != nil {
		log.Fatalf("Failed to validate kubeconfig: %v\n", err)
	}
}

func init() {
	rootCmd.AddCommand(addCmd)
}
