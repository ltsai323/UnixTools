#!/home/ltsai/local/usr/bin/bash
source .bashrc
tmux ls && tmux -CC at || tmux -CC new
