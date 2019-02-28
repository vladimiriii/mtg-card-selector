#! /usr/bin/env bash

# Check python version, should be over 3.6.7
ret=`python3 -c 'import sys; print("%i" % (sys.hexversion<0x03060700))'`
if [ $ret -eq 0 ]; then
    echo "Required version of Python already installed."

else
    echo "You need to install Python 3.6.7"
    echo -e "Install Python 3.6.7? [y/n] \c "
    read word
    if [ $word == "y" ]; then
       if [ "$(whoami)" != "root" ]; then
          echo "You need root access"
          exit 1
       fi
       # echo "You said yes"
       echo `wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz --no-check-certificate`
       echo `tar xf Python-3.6.7.tgz`
       cd Python-3.6.7
       echo `./configure --prefix=/usr/local`
       echo `make && make altinstall`
       echo `rm Python-3.6.7.tgz`
     else
       echo "Aborting installation script."
       exit 1
    fi
fi

echo "Testing whether virtualenv is installed..."
# Test whether virtualenv is installed
ve=`command -v virtualenv`
if [ -z "$ve" ]; then
   echo "You need to install virtualenv?"
   echo -e "Install virtualenv? [y/n] \c "
   read word
   if [ $word == "y" ]; then
      echo "This will install virtualenv in your home directory"
      if [ "$(whoami)" != "root" ]; then
         echo "You need root access"
         exit 1
      fi
      echo "Installing virtualenv..."
      echo `pip3 install virtualenv`
   fi
fi
# Start virtualenv and install required packages
echo `virtualenv -p python3 venv`
currentDir=`pwd`
virtualenvPath='venv/bin/activate'
source $currentDir/$virtualenvPath

pip install -r requirements.txt
echo "Installation complete."
