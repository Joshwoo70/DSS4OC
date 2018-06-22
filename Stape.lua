---
--- Created by Ristelle.
--- DateTime: 18/3/2018 4:03 PM
---
local file = io.open('config.cfg','a')
local component = require("component")
local params = {...}
if params[1] == "play" then
    local tapes = {}
    for k,v in component.list() do
        if v == "tape_drive" then
            table.insert(tapes, component.proxy(k))
        end
    end
    for k,tape in pairs(tapes) do
        tape.play()
    end
end
if params[1] == "seek" then

    for k,v in component.list() do if v == "tape_drive" then component.proxy(k).seek(tonumber(params[2])) end end
end
if params[1] == "stop" then
    for k,v in component.list() do if v == "tape_drive" then component.proxy(k).stop() end end
    for k,v in component.list() do if v == "tape_drive" then component.proxy(k).seek(-1000000000000000000000) end end
end
if params[1] == "volume" then
    local v = tonumber(params[2])
    if not v or v < 0 or v > 1 then
        io.stderr:write("Volume needs to be a number between 0.0 and 1.0")
    end
    for k,z in component.list() do if v == "tape_drive" then component.proxy(k).setVolume(v) end end
end