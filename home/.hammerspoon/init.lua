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


--------------------
-- resize windows --
--------------------

-- set full height
hs.hotkey.bind(hyper, "y", updateWindowFrame(function (w, s)
    w.y = 0
    w.h = s.h
end))

-- set half height
hs.hotkey.bind(hyper, "n", updateWindowFrame(function (w, s)
    w.h = s.h / 2
end))

-- set full width
hs.hotkey.bind(hyper, "j", updateWindowFrame(function (w, s)
    w.x = 0
    w.w = s.w
end))

-- set half width
hs.hotkey.bind(hyper, "g", updateWindowFrame(function (w, s)
    w.w = s.w / 2
end))

-- set 5/8 width
hs.hotkey.bind(hyper, "h", updateWindowFrame(function (w, s)
    w.w = 5.0 / 8.0 * s.w

    if w.x + w.w > s.w then
        w.x = s.w - w.w
    end
end))
