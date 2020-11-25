# k8vault
k8vault is a tool to securely store and access kubernetes configuration files. It stores kubeconfigs in your operating system's keystore and overwrites the ```~/.kube/config``` file when you want to use a kubeconfig. For this to work, you need the KUBECONFIG env var pointed at ```~/.kube/config```.

## Installing
You can grab a pre-compiled version of k8vault in the release tab or generate your own:
```bash
go get -u github.com/jdamata/k8vault
```

## Usage
```bash
  k8vault                                                    : Display usage
  k8vault add ~/.kube/docker-for-desktop                     : Add a kubeconfig
  k8vault add ~/.kube/docker-for-desktop --keychain jdamata  : Add a kubeconfig to the jdamata keychain
  k8vault get docker-for-desktop                             : Get a kubeconfig named docker-for-desktop
  k8vault list                                               : List kubeconfigs
  k8vault delete docker-for-desktop                          : Delete a kubeconfig
  k8vault delete --all --keychain jdamata                    : Delete all kubeconfigs in the jdamata keychain
```

## Known Issues
- K8vault doesn't support Windows Credential Manager due to the maximum password length of 127 characters.
- We store the actively used kubeconfig in ~/.kube/config. It would be better if nothing neeeded to be dropped into the filesystem. Something like a base64 encoded kubeconfig stored as an environment variable might work. Currently kubectl doesn't support this. More info here: https://github.com/kubernetes/kubernetes/issues/93346
