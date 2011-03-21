alias lch='loop chrome'
alias lcs='loop c-sharp'
alias lm='loop markdown'
alias lno-='loop nose `find . -name "*.py"`'
lno() {lno- $@ --cover-package=$(basename $(pwd))}
alias lo='loop "octave --silent {main_file} {args}"'
alias lp='loop "python -3 {main_file} {args}"'
alias lpy='loop "python {main_file} {args}"'
alias lp3='loop "python3 {main_file} {args}"'
alias lsa='loop safari'
