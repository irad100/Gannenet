tell application "System Events"
    set activeApp to name of first application process whose frontmost is true
    return activeApp
end tell