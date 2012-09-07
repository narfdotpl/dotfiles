tell application "System Events"
    if (count every process whose name is "Xcode") is 0 then
        tell application "MacVim" to activate
    else
        tell application "Xcode" to activate
    end if
end tell
