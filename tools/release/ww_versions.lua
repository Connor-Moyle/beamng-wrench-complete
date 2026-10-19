-- Wrench Works version check. The release script adds this file to every Wrench Works zip; the copies are identical,
-- so whichever one the game mounts runs once. Each mod's mod_info lists what it needs ("requires": {id = "min version"}).
local M = {}

local function parse(v)
  local t = {}
  for n in tostring(v or ''):gmatch('%d+') do t[#t + 1] = tonumber(n) end
  return t
end

local function older(a, b) -- true when version a < version b
  local x, y = parse(a), parse(b)
  for i = 1, math.max(#x, #y) do
    if (x[i] or 0) ~= (y[i] or 0) then return (x[i] or 0) < (y[i] or 0) end
  end
  return false
end

local function problems()
  local infos, out = {}, {}
  for _, path in ipairs(FS:findFiles('/mod_info/', 'info.json', 1, false, false)) do
    local id = path:match('/mod_info/([^/]+)/info%.json$')
    local info = id and jsonReadFile(path)
    if info then infos[id] = info end
  end
  for id, info in pairs(infos) do
    for need, min in pairs(type(info.requires) == 'table' and info.requires or {}) do
      local have = infos[need]
      if not have then
        out[#out + 1] = string.format('%s needs %s %s or newer, which is not installed.', info.title or id, need, min)
      elseif older(have.version, min) then
        out[#out + 1] = string.format('%s needs %s %s or newer; you have %s.', info.title or id, have.title or need, min, tostring(have.version))
      end
    end
  end
  table.sort(out)
  return out
end

M.problems = problems
M.older = older

local warned = false
function M.onClientStartMission()
  if warned then return end
  warned = true
  for _, msg in ipairs(problems()) do
    log('W', 'ww_versions', msg)
    guihooks.trigger('toastrMsg', { type = 'warning', title = 'Wrench Works', msg = msg, config = { timeOut = 0 } })
  end
end

return M
