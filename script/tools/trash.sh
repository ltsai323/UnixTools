# create the trash bin.
# need to add 'rm ~/.trash/* -r' in the .bash_logout
# Then the file will altomatically remove.
1. mkdir ~/.trash
2. echo "alias rm='mv -t  ~/.trash/ '" >> ~/.bashrc
3. echo "/bin/rm -r ~/.trash/*"        >> ~/.bash_logout



