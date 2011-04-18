let current_compiler = "pyflakes"

if exists(":CompilerSet") != 2
    command -nargs=* CompilerSet setlocal <args>
endif

CompilerSet errorformat=%f:%l:\ %m
CompilerSet makeprg=pyflakes\ %
