# always use hyper
bind = (key, x) ->
    slate.bind "#{key}:shift;ctrl;alt;cmd", x

# open apps quickly
for [key, app] in [
    ['a', 'iTerm'],
    ['s', 'MacVim'],
    ['d', 'Google Chrome'],
    ['e', 'Spotify'],
    ['r', 'HipChat'],
    ['f', 'Clear'],
    ['v', 'Twitter'],
]
    do (app) ->
        bind key, -> slate.shell("/usr/bin/open -a '#{app}'")

# show hints
bind 'z', slate.operation 'hint',
    characters: 'asdwqxcef'

# move windows
for [key, directions] in [
    ['i', ['up', 'left']],
    ['o', ['up', 'right']],
    ['k', ['down', 'left']],
    ['l', ['down', 'right']],
]
    operations = []
    for direction in directions
        operations.push([slate.operation('push', direction: direction)])

    bind key, slate.operation('sequence', operations: operations)

# show grid
bind 'h', slate.operation 'grid',
    grids:
        '1920x1080':
            width: 6
            height: 6
        '1440x900':
            width: 4
            height: 4

# resize windows
defaults =
    x: 'windowTopLeftX'
    y: 'windowTopLeftY'
    width: 'windowSizeX'
    height: 'windowSizeY'
for [key, obj] in [
    ['y', height: 'screenSizeY', y: 'screenOriginY'],
    ['g', width: 'screenSizeX / 2'],
    ['j', width: 'screenSizeX', x: 'screenOriginX'],
    ['b', height: 'screenSizeY / 2'],
    ['n', height: 'screenSizeY / 2'],
]
    bind key, slate.operation('move', _({}).extend(defaults, obj))

# use spotify maximized on the smaller monitor
slate.default ['1920x1080', '1440x900'], slate.layout 'foo',
    Spotify:
        operations: [
            slate.operation 'move',
                screen: 1
                x: 'screenOriginX'
                y: 'screenOriginY'
                width: 'screenSizeX'
                height: 'screenSizeY'
        ]

# move window between primary and secondary monitor
bind 'm', (win) ->
    win.doOperation slate.operation 'throw',
        screen: (slate.screen().id() + 1) % 2
