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
	var allowedbackends = []keyring.BackendType{
		keyring.KeychainBackend,
		keyring.SecretServiceBackend,
		keyring.KWalletBackend,
		keyring.PassBackend,
		keyring.FileBackend,
	}
		
	ring, err := keyring.Open(keyring.Config{
		AllowedBackends:          allowedbackends,
		ServiceName:              "k8vault",
		KeychainTrustApplication: true,
		KeychainName:             KeychainName,
		FileDir:                  "~/.k8vault/keys/",
		KWalletAppID:             "k8vault",
		KWalletFolder:            "k8vault",
		LibSecretCollectionName:  "k8vault",
})
	if err != nil {
		log.Fatalf("Failed to open keyring: %v\n", err)
	}
	return ring
}
