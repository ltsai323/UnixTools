#!/home/ltsai/local/usr/bin/bash
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
source .bashrc
# automatically detach other sessions by -d option
tmux ls && tmux -CC at -d || tmux -CC new

