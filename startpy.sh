!#/bin/sh
REQUIRED_PKG="python3.8"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "$REQUIRED_PKG is not installed. Installing $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG 
fi
python3.8 botstart.py
