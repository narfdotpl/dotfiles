------------
-- config --
------------

hyper = {"shift", "ctrl", "alt", "cmd"}

-- reload config on change
configWatcher = hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon", hs.reload)
configWatcher:start()


---------------
-- open apps --
---------------

for key, app in pairs({
    a="iTerm",
    s="MacVim",
    d="Safari",
    e="Spotify",
    f="Visual Studio Code",
    c="Blender",
    v="Things3",
}) do
    hs.hotkey.bind(hyper, key, function()
        hs.application.launchOrFocus(app)
    end)
end


------------------
-- move windows --
------------------

function updateWindowFrame(callback)
    return function()
        local win = hs.window.focusedWindow()
        local w = win:frame()
        local s = win:screen():frame()

        callback(w, s)
        win:setFrame(w)
    end
end

-- move window to top left
hs.hotkey.bind(hyper, "i", updateWindowFrame(function (w, s)
    w.x = 0
    w.y = 0
end))

-- move window to top right
hs.hotkey.bind(hyper, "o", updateWindowFrame(function (w, s)
    w.x = s.w - w.w
    w.y = 0
end))

-- move window to bottom left
hs.hotkey.bind(hyper, "k", updateWindowFrame(function (w, s)
    w.x = 0
    w.y = s.h - w.h
end))

-- move window to bottom right
hs.hotkey.bind(hyper, "l", updateWindowFrame(function (w, s)
    w.x = s.w - w.w
    w.y = s.h - w.h
end))

-- center window
hs.hotkey.bind(hyper, "b", updateWindowFrame(function (w, s)
    w.x = (s.w - w.w) / 2
    w.y = (s.h - w.h) / 2
end))

-- move window on one axis at a time, stopping at the center
function moveWindow(dx, dy)
    return updateWindowFrame(function (w, s)
        local xLeft = s.x
        local xRight = s.w - w.w
        local xCenter = (xRight - xLeft) // 2

        if dx < 0 then
            w.x = w.x <= xCenter and xLeft or xCenter
        elseif dx > 0 then
            w.x = xCenter <= w.x and xRight or xCenter
        end

        local yTop = s.y
        local yBottom = s.h - w.h
        local yCenter = (yBottom - yTop) // 2

        if dy < 0 then
            w.y = w.y <= yCenter and yTop or yCenter
        elseif dy > 0 then
            w.y = yCenter <= w.y and yBottom or yCenter
        end
    end)
end

hs.hotkey.bind(hyper, "left", moveWindow(-1, 0))
hs.hotkey.bind(hyper, "right", moveWindow(1, 0))
hs.hotkey.bind(hyper, "up", moveWindow(0, -1))
hs.hotkey.bind(hyper, "down", moveWindow(0, 1))


--------------------
-- resize windows --
--------------------

-- set height
for key, ratio in pairs({
    n=1/2,
    y=1,
}) do
    hs.hotkey.bind(hyper, key, updateWindowFrame(function (w, s)
        w.h = ratio * s.h

        if w.y + w.h > s.h then
            w.y = s.h - w.h
        end
    end))
end

-- set width
for key, ratio in pairs({
    g=1/2,
    u=1/3,
    h=2/3,
    j=1,
}) do
    hs.hotkey.bind(hyper, key, updateWindowFrame(function (w, s)
        w.w = ratio * s.w

        if w.x + w.w > s.w then
            w.x = s.w - w.w
        end
    end))
end
