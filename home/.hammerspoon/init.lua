------------
-- config --
------------

hyper = {"shift", "ctrl", "alt", "cmd"}

-- make it easier for ZMK keymap renderer to figure out key labels
function bindHyper(key, label, fn)
    hs.hotkey.bind(hyper, key, fn)
end

-- reload config on change
configWatcher = hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon", hs.reload)
configWatcher:start()


---------------
-- open apps --
---------------

for key, app in pairs({
    t="Finder",

    a="Obsidian",
    b="Signal",

    d="cmux",
    e="Ghostty",
    f="Safari",
    g="Visual Studio Code",

    h="Blender",
    i="Xcode",
    j="MacVim",
    k="Things3",
    l="Ableton Live 12 Suite",
}) do
    hs.hotkey.bind(hyper, key, function()
        hs.application.launchOrFocus(app)
    end)
end


-------------------------
-- change input source --
-------------------------

for key, layout in pairs({
    u="com.apple.keylayout.UnicodeHexInput",
    v="com.apple.keylayout.PolishPro",
}) do
    hs.hotkey.bind(hyper, key, function()
        hs.keycodes.currentSourceID(layout)
    end)
end


---------------------------
-- toggle grayscale mode --
---------------------------

bindHyper("w", "toggle greyscale filter", function()
    hs.shortcuts.run("Toggle Color Filters")
end)


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

-- center window
bindHyper("y", "center", updateWindowFrame(function (w, s)
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

bindHyper("left",  "←", moveWindow(-1, 0))
bindHyper("right", "→", moveWindow(1, 0))
bindHyper("up",    "↑", moveWindow(0, -1))
bindHyper("down",  "↓", moveWindow(0, 1))


--------------------
-- resize windows --
--------------------

-- set height
function setRelativeWindowHeight(ratio)
    return updateWindowFrame(function (w, s)
        local oldRatio = w.h / s.h

        w.h = ratio * s.h

        -- center
        if oldRatio == 1 and ratio < 1 then
            w.y = (s.h - w.h) / 2
            return
        end

        local isOverTheEdge = w.y + w.h > s.h
        if isOverTheEdge then
            w.y = s.h - w.h
        end
    end)
end

bindHyper("n", "H:1/2", setRelativeWindowHeight(1/2))
bindHyper("m", "H:1",   setRelativeWindowHeight(1))

-- set width
function setRelativeWindowWidth(ratio)
    return updateWindowFrame(function (w, s)
        local oldRatio = w.w / s.w
        local wasOnRightEdge = w.x + w.w >= s.w - 2

        w.w = ratio * s.w

        -- center
        if oldRatio == 1 and ratio < 1 then
            w.x = (s.w - w.w) / 2
            return
        end

        local isOverTheEdge = w.x + w.w > s.w
        if wasOnRightEdge or isOverTheEdge then
            w.x = s.w - w.w
        end
    end)
end

bindHyper("o", "W:2/6", setRelativeWindowWidth(2/6))
bindHyper("p", "W:3/6", setRelativeWindowWidth(3/6))
bindHyper("q", "W:4/6", setRelativeWindowWidth(4/6))
bindHyper("r", "W:5/6", setRelativeWindowWidth(5/6))
bindHyper("s", "W:6/6", setRelativeWindowWidth(6/6))

-- resize window to 2/3x1 and center it
bindHyper("x", "center W:2/3 H:1", updateWindowFrame(function (w, s)
    w.w = 2/3 * s.w
    w.h = s.h

    w.x = (s.w - w.w) / 2
    w.y = s.y
end))

-- resize window to 1/2x1/2 and center it
bindHyper("z", "center W:1/2 H:1/2", updateWindowFrame(function (w, s)
    w.w = 1/2 * s.w
    w.h = 1/2 * s.h

    w.x = (s.w - w.w) / 2
    w.y = (s.h - w.h) / 2
end))
