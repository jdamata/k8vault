package cmd

import (
	"github.com/99designs/keyring"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	keychain string
	rootCmd  = &cobra.Command{
		Use:   "k8vault",
		Short: "Secure storage of kubeconfigs",
		Long:  "K8vault is a CLI that allows secure storage of kubeconfigs in OS keystores.",
	}
)

// Execute executes the root command.
func Execute(version string) error {
	rootCmd.Version = version
	rootCmd.PersistentFlags().StringVarP(&keychain, "keychain", "k", "k8vault", "Name of the keychain to use")
	viper.BindPFlag("keychain", rootCmd.Flags().Lookup("keychain"))
	return rootCmd.Execute()
}

func logging() {
	log.SetFormatter(&log.TextFormatter{
		DisableColors: true,
		FullTimestamp: true,
	})
}

func openRing(KeychainName string) keyring.Keyring {
	ring, err := keyring.Open(keyring.Config{
		ServiceName:              "k8vault",
		KeychainTrustApplication: false,
		KeychainName:             KeychainName,
	})
	if err != nil {
		log.Fatal("Failed to open keyring\n", err)
	}
	return ring
}
