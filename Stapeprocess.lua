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
local compare = ""

local function bytes_to_int(str,endian,signed) -- use length of string to determine 8,16,32,64 bits
    local t={str:byte(1,-1)}
    if endian=="big" then --reverse bytes
        local tt={}
        for k=1,#t do
            tt[#t-k+1]=t[k]
        end
        t=tt
    end
    local n=0
    for k=1,#t do
        n=n+t[k]*2^((k-1)*8)
    end
    if signed then
        n = (n > 2^(#t*8-1) -1) and (n - 2^(#t*8)) or n -- if last bit set, negative.
    end
    return n
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
    else
        io.stderr:write("Invalid URL.")
        return false
    end
    local count = 0
    local tapes = {}
    for k,v in component.list() do
        if v == "tape_drive" then
            count = count + 1
            table.insert(tapes,component.proxy(k))
        end
    end
    local handler = internet.request(params[2])
    local buffer = handler:read(7)
    if buffer ~= "\000DFPWMX" then
        io.stderr:write("Not valid DFPWMX.")
    end
    buffer = handler:read(2)
    local mixedstream = false
    local bytes = 2048
    local files = 0
    if buffer[1] == "B" then
        if buffer[2] == "\002" then
            mixedstream = true
            bytes = bytes_to_int(handler:read(4),'big',false)
        end
    end
    buffer = handler:read(2)
    if buffer[2] == "F" then
        files = bytes_to_int(handler:read(2),'big',false)
        if files ~= #tapes then
            io.stderr:write("Incorrect balanced tapes requested: \"" + files + "\". Got: \"" + #tapes + "\".")
            return false
        end
    end
    handler:read(1)
    local sizes = {}
    for i = 1, #tapes do
        table.insert(sizes,bytes_to_int(handler:read(4),'big',false))
    end
    buffer = ""
    while buffer ~= 0xff do
        buffer = handler:read(1)
    end
    if ~mixedstream then
        while true do
            if sizes[1] == 0 then
                table.remove(sizes,1)
                table.remove(tapes,1)
            end
            buffer = handler:read(sizes[1])
            if buffer == "" then
                return true
            end
            sizes[1] = sizes[1] - #buffer
            tapes[1].write(buffer)
        end
    elseif mixedstream then

    else
        io.stderr:write("Schrodinger's state detected. Cannot determine whether mixedstream is there or not.")
    end
end