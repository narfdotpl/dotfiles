# always use hyper
bind = (key, x) ->
    slate.bind "#{key}:shift;ctrl;alt;cmd", x

# open apps quickly
for [key, app] in [
    ['a', 'iTerm'],
    ['s', 'MacVim'],
    ['d', 'Google Chrome'],
    ['e', 'Spotify'],
    ['r', 'Messenger'],
    ['f', 'Xcode'],
    ['x', 'Simulator'],
    ['c', 'Simulator'],
    ['v', 'Clear'],
]
    do (app) ->
        bind key, -> slate.shell("/usr/bin/open -a '#{app}'")

# control Spotify with media keys remapped in KeyRemap4MacBook to Hyper+NumPad
for [key, cmd] in [
    ['pad7', 'previous track'],
    ['pad8', 'playpause'],
    ['pad9', 'next track'],
]
    do (cmd) ->
        bind key, -> slate.shell("/users/narf/bin/tell spotify to #{cmd}")

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
        '1920x1200':
            width: 6
            height: 6
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

# move window between primary and secondary monitor, preserving maximization
bind 'm', (win) ->
    # fail fast
    return if not win

    # get screen dimensions
    screenRect = win.screen().rect()
    screenWidth = screenRect.width
    screenHeight = screenRect.height

    # set thresholds
    menuBarHeight = 23
    dockWidth = 90
    thresholdWidth = screenWidth - dockWidth
    thresholdHeight = screenHeight - menuBarHeight

    # get window dimensions
    {width, height} = win.size()

    # move window
    win.doOperation slate.operation 'throw',
        screen: (slate.screen().id() + 1) % 2

    # maximize window
    win.doOperation slate.operation 'move',
        x: 'windowTopLeftX'
        y: 'windowTopLeftY'
        width: if width >= thresholdWidth then 'screenSizeX' else width
        height: if height >= thresholdHeight then 'screenSizeY' else height
