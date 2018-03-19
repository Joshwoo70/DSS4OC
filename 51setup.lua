---
--- Created by Ristelle.
--- DateTime: 18/3/2018 4:03 PM
---
local file = io.open('config.cfg','a')
local component = require("component")
local steps = {'Left Front','Left Back','Center','Right Front','Right Back'}

local function checker()
    for address in component.list("tape_drive") do
            if component.proxy(address).isReady() == true then
                file.write(address + '|' + step + '\n')
                print("Found at address:" + address)
                return true
            end

        end
    return false
end

for step in steps do
    print("Put Tape into \""+ step +"\" Drive and then press enter to detect.")
    io.read()
    while true do
        if checker() == true then
            break
        else
            print("Failed to find\"" + step + "\". Try again.")
            io.input()
        end
    end
end

