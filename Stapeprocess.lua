---
--- Created by Ristelle.
--- DateTime: 18/3/2018 4:03 PM
---
local file = io.open('config.cfg','a')
local component = require("component")
local params = {...}
local function printUsage()
    print(" - 'tape write <URL>' to write from a URL")
end
if params[1] == "write" then
    if params[3] == "" then
        print("No URL Specified.")
        return
    end
    if string.match(params[2], "https?://.+") then
        if not component.isAvailable("internet") then
            io.stderr:write("This command requires an internet card to run.")
            return false
        end
    end
    for k,v in component.list() do
        if v == "tape_drive" then
            component.proxy(k).play()
        end
    end

end