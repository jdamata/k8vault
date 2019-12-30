package cmd

import (
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
	ring := openRing("k8vault")

	if viper.GetBool("deleteAll") {
		keys, _ := ring.Keys()
		if len(keys) < 1 {
			log.Fatal("There are no configs to delete")
		}
		if yesNo() {
			for _, config := range keys {
				deleteConfig(ring, config)
			}
		}
		os.Exit(0)
	}

	if len(args) == 1 {
		deleteConfig(ring, args[0])
	} else {
		log.Error("Either config does not exists in the keyring or a config was not specified")
		cmd.Help()
	}
}

func yesNo() bool {
	prompt := promptui.Select{
		Label: "Do you want to purge all kubeconfigs? Select[Yes/No]",
		Items: []string{"Yes", "No"},
	}
	_, result, err := prompt.Run()
	if err != nil {
		log.Fatalf("Prompt failed %v\n", err)
	}
	return result == "Yes"
}

func deleteConfig(ring keyring.Keyring, config string) {
	err := ring.Remove(config)
	if err != nil {
		log.Fatal(err)
	}
	log.Info("Deleted config: ", config)
}

func init() {
	deleteCmd.Flags().BoolP("all", "a", false, "Delete all kubeconfigs")
	viper.BindPFlag("deleteAll", deleteCmd.Flags().Lookup("all"))
	rootCmd.AddCommand(deleteCmd)
}
