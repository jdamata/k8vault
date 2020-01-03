package cmd

import (
	"fmt"
	"os"
	"text/tabwriter"

	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List kubeconfigs in the keychain",
	Run:   listKubeconfig,
}

func listKubeconfig(cmd *cobra.Command, args []string) {
	ring := openRing(keychain)
	keys, err := ring.Keys()
	if err != nil {
		log.Fatal("Failed listing keys\n", err)
	}
	formattedList(keys)
}

func formattedList(keys []string) {
	w := new(tabwriter.Writer)
	w.Init(os.Stdout, 0, 8, 0, '\t', 0)
	fmt.Fprintln(w, "KubeConfigs")
	fmt.Fprintln(w, "----------------")
	for _, config := range keys {
		fmt.Fprintln(w, config)
	}
	w.Flush()
}

func init() {
	rootCmd.AddCommand(listCmd)
}
