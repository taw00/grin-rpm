# grin-rpm
GRIN for Fedora

NOTE: All of this is still in testing.

This github repository contains source packages and source package bits in
order to build `grin` and `grin-miner` for Fedora Linux (and presumably
EL-based distros).

These source packages are used to build packages used to deploy runnable
binaries. Those are built on Fedora's COPR build infrastructure. Getting
access, though, is easy. Just install the repo-enabling package and install
grin or grin-miner. Here you go...

```bash
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/grin-rpm/master/toddpkgs-grin-repo.fedora.testing.rpm
sudo dnf list --refresh |grep grin
#sudo dnf install -y grin
#sudo dnf install -y grin-miner
```

Documentation on use: https://github.com/mimblewimble/docs/wiki/Getting-Started-With-Grin%3A-Links-and-Resources

## Summary: initial install

To run a wallet, you need to connect to a node. So, first install a node
locally (you can point at a remote node, but that is beyond the scope of this
document).

To run a miner, you need to 

### Grin Node:
1. Install the `grin` package: `sudo dnf install grin`
2. Create a `grin` directory and add it to your path...
```
cd ~
mkdir grin
echo export 'PATH=~/grin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Grin Wallet:


Good luck!
-t0dd or taw in most chat platforms and forums
