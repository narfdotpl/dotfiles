" preview js
autocmd FileType coffee :map <buffer> <Leader><Space> :CoffeeCompile<Enter>

" use coffeelint config
let coffee_lint_options = '-f ~/.vim/bundle/coffeescript-settings/coffeelint.json'

" run coffeelint on save
autocmd BufWritePost *.coffee :CoffeeLint | cwindow
