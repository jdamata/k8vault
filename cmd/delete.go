package cmd

import (
	"fmt"
	"os"

	"github.com/99designs/keyring"
	"github.com/manifoldco/promptui"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	deleteAll bool
	deleteCmd = &cobra.Command{
		Use:   "delete [CONFIGNAME]",
		Short: "Delete a kubeconfig from the keychain",
		Run:   deleteKubeconfig,
	}
)

func deleteKubeconfig(cmd *cobra.Command, args []string) {
	ring := openRing(keychain)
	if viper.GetBool("deleteAll") {
		purgeAll(ring)
	}
	if len(args) == 1 {
		deleteConfig(ring, args[0])
	} else {
		cmd.Help()
	}
}

func purgeAll(ring keyring.Keyring) {
	keys, _ := ring.Keys()
	if len(keys) < 1 {
		log.Fatal("There are no configs to delete")
	}
	result := prompt("Do you want to purge all kubeconfigs? Select[Yes/No]")
	if result == "yes" {
		for _, config := range keys {
			deleteConfig(ring, config)
		}
	}
	os.Exit(0)
}

func deleteConfig(ring keyring.Keyring, config string) {
	result := prompt(fmt.Sprintf("Do you want to delete config %s? Select[Yes/No]", config))
	if result == "Yes" {
		err := ring.Remove(config)
		if err != nil {
			log.Fatalf("Failed to delete kubeconfig: %v\n", err)
		}
		log.Infof("Deleted config: %v\n", config)
	}
}

func prompt(message string) string {
	prompt := promptui.Select{
		Label: message,
		Items: []string{"Yes", "No"},
	}
	_, result, err := prompt.Run()
	if err != nil {
		log.Fatalf("Prompt failed: %v\n", err)
	}
	return result
}

func init() {
	deleteCmd.Flags().BoolP("all", "a", false, "Delete all kubeconfigs")
	viper.BindPFlag("deleteAll", deleteCmd.Flags().Lookup("all"))
	rootCmd.AddCommand(deleteCmd)
}
