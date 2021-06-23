#!/home/ltsai/local/usr/bin/bash
source .bashrc
# automatically detach other sessions by -d option
tmux ls && tmux -CC at -d || tmux -CC new
