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

Documentation on usage: <https://github.com/mimblewimble/docs/wiki/Getting-Started-With-Grin%3A-Links-and-Resources>

## Summary usage

### I want to initialize and use a wallet

**Initialize (create) a wallet?** Easy peasy...

```
# At the commandline as a normal user...
grin wallet init
```

You will be asked for a password. Enter that twice and a seed will be
generated. Backup these two pieces of data somewhere.

Done! Wallet created. All data is stored, by default, in `~/.grin/`

**Use a wallet?**

To use a grin wallet, you need to connect to a node. The easy means to do that
is to run your own! Your local wallet will, by defaul, look for a local full
node to connect to. So skip to that step, and when you get a full node running,
come back here.

...you switch terminals and start up a full grin node...

Ready to use the wallet? Got a running node in another terminal? Great.

Try this...
```
grin wallet info
grin wallet help
```

That will get you started, but... better to read how to use a wallet
[here](https://github.com/mimblewimble/docs/wiki/how-to-use-the-grin-wallet#checking-your-wallet-balance).

### I want to run a node

Run a node to help secure the network... and because you need a full node in
order to use your wallet. You _could_ connect to any node out there that will
allow you to, but ... let's run one locally and use that!

Again, this is so easy! Open up a different terminal than your wallet and...

```
grin
```

Yup. That's it! Type in the `grin` command and a graphical-ish dashboard comes
up and you are rolling.

Again, all data is stored, by default, in `~/.grin/`
to run your own node and then have your wallet connect to it.


### I want to run a grin miner

1. Terminal window one:
   - Get a node running (see above)
   - Shut it down: `q`
   - Edit `~/.grin/main/grin-server.toml`
   - Change `enable_stratum_server = false` to `enable_stratum_server = true`
   - Set the grin node again: `grin`
2. Terminal window two:
   - Create a wallet if you haven't already (see above)
   - Run the wallet in listening mode `grin wallet listen`
   - The wallet will stay running.
4. Terminal window three:  
   The grin miner is a bit more quirky than the rest, so... pay attention!
   - Copy the default `grin-miner.toml` file to your local data directory...  
     ```
     cp /var/lib/grin/grin-miner.toml ~/.grin/
     ```
   - Change the plugins directory (if it isn't already) to `/var/lib/grin/plugins`  
     Note: this will be done for you in v1.0.1-0.2  
     `miner_plugin_dir = "target/debug/plugins"` to  
     `miner_plugin_dir = "/var/lib/grin/plugins"`
   - Change the mining algorithm if you know what you are doing. Read more
     about that
     [here](https://github.com/mimblewimble/docs/wiki/how-to-mine-grin#configure-grin-miner)
   - Run the miner from the `.grin` directory. Yup. Odd, but that is the way it is...  
     ```
     cd ~/.grin
     grin-miner
     ```

That sums it all up!


Good luck!
-t0dd or taw in most chat platforms and forums

...

Check out my other crypto-oriented RPM builds:
- Dash (my longest running and tested builds): https://github.com/taw00/dashcore-rpm
- Electrum-Dash (somewhat experimental): https://github.com/taw00/electrum-dash-rpm
- ZCash: https://github.com/taw00/dashcore-rpm
- Beam: https://github.com/taw00/beam-rpm
- IPFS (somewhat experimental): https://github.com/taw00/ipfs-rpm

