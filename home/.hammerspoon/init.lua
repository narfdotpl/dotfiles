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
    f="Visual Studio Code",

    e="Spotify",

    x="Ableton Live 11 Standard",
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

        -- move Slack almost off screen, so that only a split view is visible
        local xSlackLeft = -w.w + s.w // 6 + 25

        local xSteps = {xSlackLeft, xLeft, xCenter, xRight}

        if dx < 0 then
            for i = #xSteps, 1, -1 do
                local x = xSteps[i]
                if w.x > x then
                    w.x = x
                    break
                end
            end
        elseif dx > 0 then
            for _, x in pairs(xSteps) do
                if w.x < x then
                    w.x = x
                    break
                end
            end
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
    end))
end
