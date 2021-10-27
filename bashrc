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
#source /cvmfs/cms-ib.cern.ch/latest/cmsset_default.sh

# User specific aliases and functions

# export SCRAM_ARCH=slc7_amd64_gcc630    # open it when you login lxplus7
#export SCRAM_ARCH=slc7_amd64_gcc820   # not able used due to ntu version
export SCRAM_ARCH=slc7_amd64_gcc700
export QLOGDIR=/home/ltsai/Work/qjob/qSubMessage/
#export PATH=${PATH}:${HOME}/local/bin
export PATH=${HOME}/local/bin:${HOME}/local/usr/bin:${PATH}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${HOME}/local/usr/lib/
#export PYTHONPATH=$PYTHONPATH:/home/ltsai/local/mylib/python

# force to 256 color (in order to use color in tmux
export TERM='xterm-256color'
source ${HOME}/.iterm2_shell_integration.bash
# change the format of the command line
export PS1='\[\e[0;37m\]\u@\h:\[\e[1;34m\]\w\[\e[0;38m\]\n > '
export EDITOR=/home/ltsai/local/bin/nvim
export NCHCHEADER='root://se01.grid.nchc.org.tw/'




myScriptBase=${HOME}/script
alias Date="$myScriptBase/tools/Updater.sh"
alias HISTORYRECORD='vim /home/ltsai/Work/history/Update.txt'
alias voupdater="  source $myScriptBase/tools/renewVO.sh" 
alias envoupdater="source $myScriptBase/tools/renewVOToENV.sh" 
alias ll='ls -l'
alias ls='ls --color=auto'
alias lt='ls --color=auto -tr'
alias LS='ls --color=auto -lh'
alias la='ls --color=auto -a'
alias Note="$myScriptBase/tools/Note.sh"
alias ScramRun='cd $CMSSW_BASE/src && scram b -j4 && cd - && cmsRun '
alias SCRAM='cd $CMSSW_BASE/src&&scram b -j4&&cd -'
alias SearchContent="$myScriptBase/tools/scanFile.sh "
alias nchcview="$myScriptBase/CRAB/viewNCHC.py"
#alias nchcdownload="$myScriptBase/CRAB/downloadNCHC.py"
alias nchcdownload="sh $myScriptBase/CRAB/nchcdwn.sh"
alias nchcmkdir="$myScriptBase/CRAB/mkdirInNCHC.py"
alias nchcrm="$myScriptBase/CRAB/rmNCHC.py"
alias a="$myScriptBase/tools/g++CompileRun.sh "
alias astyle='~/local/usr/bin/astyle  --style=allman'
#alias tmux='tmux -2' # for 256 color output
alias cmsenv='eval `scramv1 runtime -sh`'
alias cmsrel='scramv1 project CMSSW'
alias crabcheckWrite='/home/ltsai/script/CRAB/crabCheckWrite.sh'
alias g++11='g++ -std=c++0x -o a'
alias groot="$myScriptBase/tools/compileGRoot.sh "
alias grootfit="$myScriptBase/tools/compileGRooFit.sh " 
alias lxplus='ssh lxplus'
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
alias show='eog'
alias icat='imgcat'
alias vi='nvim -X'
alias vis='nvim -X -p'
alias vim='vim -X'
alias qjobs='qstat -u ltsai'
alias qalljobs='qstat'
alias qclearlog='~/script/qjob/clearQJOBmessageDirectory.py --delete'
alias qlog='~/script/qjob/clearQJOBmessageDirectory.py'
alias qkill='qdel -u $USER all'
alias root='root -b'
alias qroot='root -b -q'
alias figroot='unalias root; alias root="root -l"'
alias log='less log'
#alias rmfig='rm /home/ltsai/Work/LbFrame/workspace/store_fig/*'
alias rmfig='rm /home/ltsai/Work/workspaceGammaPlusJet/storefig/*' # for ggAnalysis
alias rmqjobhistory='rm /home/ltsai/Work/qjob/qSubMessage/* ; rm /home/ltsai/Work/qjob/qSubResult/*'
alias timerecord='/home/ltsai/script/tools/scheduleRecorder.py'
alias rmtrash='/bin/rm -rf ~/.trash/* '
alias grep='grep --color=always'
alias GREP='/bin/grep'
alias TBrowser="sh ~/script/tools/tbrowsing.sh"
alias findpath='python  ~/script/tools/LocallyBrowseRootFiles.py'
