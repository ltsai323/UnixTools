source .bashrc
# detach other connection by -d option
tmux ls && tmux -2 at -d || tmux new -2
