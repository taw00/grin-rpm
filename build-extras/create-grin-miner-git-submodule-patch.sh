# This is used to create the patch file needed in order to build the grin-mw-miner RPM
# -todd warner
_date_Ym=$(date +%Y-%m)
_date_F=$(date +%F)
_date=$_date_F
_version="2.0.0"
_patchname="grin-miner-$_version-git-submodule-update-init-$_date.patch"

echo "Did you do this first?"
echo "1. Download grin-miner-$_version.tar.gz"
echo "2. Copy it to here and tar -xvzf grin-miner-$_version.tar.gz"
echo
echo "Then this script will do this (essentially)..."
echo "git clone https://github.com/mimblewimble/grin-miner.git grin-miner-copy"
echo "# Or if you have it checked out already: cp -a grin-miner grin-miner-copy"
echo "cd grin-miner-copy"
echo "git pull ; git submodule update --init"
echo "cd .."
echo "rm -rf grin-miner-copy"
echo
echo "...and then..."
echo "diff -urN --exclude=".git" grin-miner-$_version grin-miner-copy > $_patchname"
echo

git clone https://github.com/mimblewimble/grin-miner.git grin-miner-copy
cd grin-miner-copy
git submodule update --init
cd ..
diff -urN --exclude=".git" grin-miner-$_version grin-miner-copy > $_patchname
rm -rf grin-miner-copy

echo "patch created: $(ls -lh ${_patchname})"
