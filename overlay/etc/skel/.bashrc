# ~/.bashrc: executed by bash(1) for non-login shells.
# Luca OS custom shell profile

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# History control
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=10000
HISTFILESIZE=20000
shopt -s checkwinsize

# Colored Prompt
if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    color_prompt=yes
else
    color_prompt=
fi

if [ "$color_prompt" = yes ]; then
    PS1='\[\033[01;36m\]\u@luca-pc\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='\u@luca-pc:\w\$ '
fi
unset color_prompt

# Enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# Luca OS aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias luca-setup='luca-android-setup'
alias luca-help='luca-welcome'
alias apk-install='luca-apk-install'
alias waydroid-start='waydroid session start'
alias waydroid-stop='waydroid session stop'
alias waydroid-restart='sudo systemctl restart waydroid-container'

# Display system info on interactive launch
if [ -x /usr/local/bin/luca-sysinfo ]; then
    /usr/local/bin/luca-sysinfo
fi
