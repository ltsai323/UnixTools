# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# use for scp. prevent "echo" to crash scp
if [ -z "$PS1" ]; then
    return
fi

source /cvmfs/cms.cern.ch/cmsset_default.sh 

# User specific aliases and functions

export PATH=${PATH}:${HOME}/local/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${HOME}/local/usr/lib/

# force to 256 color (in order to use color in tmux
export TERM='xterm-256color'
# change the format of the command line
export PS1='\[\e[0;37m\]\u@\h:\[\e[1;34m\]\w\n\[\e[0;38m\]  cmd > '


alias Date='~/script/tools/Updater.sh'
alias HISTORYRECORD='vim /home/ltsai/Work/history/Update.txt'
alias VOrefresh='~/script/tools/renewVO.sh' 
alias ll='ls -l'
alias ls='ls --color=auto'
alias lt='ls --color=auto -tr'
alias LS='ls --color=auto -lh'
alias la='ls --color=auto -a'
alias Note='~/script/tools/Note.sh'
alias ScramRun='cd $CMSSW_BASE/src && scram b -j4 && cd - && cmsRun '
alias SCRAM='cd $CMSSW_BASE/src&&scram b -j4&&cd -&& '
alias SearchContent='~/script/tools/scanFile.sh '
alias a='~/script/tools/g++CompileRun.sh '
alias astyle='~/local/usr/bin/astyle  --style=allman'
alias tmux='tmux -2' # for 256 color output
alias cmsenv='eval `scramv1 runtime -sh`'
alias cmsrel='scramv1 project CMSSW'
alias g++11='g++ -std=c++0x -o a'
alias groot='/home/ltsai/script/tools/compileGRoot.sh ' 
alias grootfit='/home/ltsai/script/tools/compileGRooFit.sh ' 
alias lxplus='ssh ltsai@lxplus.cern.ch'
alias psmyself='ps -U ltsai'
alias node01='ssh -x node01'
alias node02='ssh -x node02'
alias node03='ssh -x node03'
alias node04='ssh -x node04'
alias node05='ssh -x node05'
alias node06='ssh -x node06'
alias node07='ssh -x node07'
alias node08='ssh -x node08'
alias node09='ssh -x node09'
alias node10='ssh -x node10'
alias node11='ssh -x node11'
alias node12='ssh -x node12'
alias node13='ssh -x node13'
alias node14='ssh -x node14'
alias node15='ssh -x node15'
alias node16='ssh -x node16'
alias node17='ssh -x node17'
alias node18='ssh -x node18'
alias node19='ssh -x node19'
alias node20='ssh -x node20'
alias nodes='$(printf "ssh -x node%02d" $((${RANDOM} % 20 + 1)))'
alias rm='mv -t ~/.trash'
alias show='gnome-open'
alias vi='~/local/usr/bin/vim -X'
alias vis='~/local/usr/bin/vim -X -p'
alias qjobs='qstat -u ltsai'
alias root='root -b'
alias qroot='root -b -q'
alias log='less log'


if [ "$HOSTNAME" == 'ntugrid5.phys.ntu.edu.tw' ]; then
    node01
elif [ "$HOSTNAME" == 'ntugrid5' ]; then
    node01
else
    echo "login into: $HOSTNAME"
fi
