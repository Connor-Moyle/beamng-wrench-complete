-- Wrench Complete: the five parts (Wrench Works, Street Legal, Drivers & Pedestrians, Driver Injuries, Car Surface FX) are inside this mod.
-- If a separate copy of one of them is also installed, its extensions would load twice: say so once, clearly, and write it to the log.
-- A separate copy shows as its own /mod_info/<name>/info.json in the mounted file system.

local M = {}

M.SEPARATE = { 'wrench_works', 'street_legal', 'slrr_drivers', 'slrr_injury', 'carSurfaceFx' }
M.NAMES = { wrench_works = 'Wrench Works', street_legal = 'Street Legal', slrr_drivers = 'Drivers & Pedestrians', slrr_injury = 'Driver Injuries', carSurfaceFx = 'Car Surface FX' }

local function names(list)
  local out = {}
  for _, id in ipairs(list) do out[#out + 1] = M.NAMES[id] or id end
  return table.concat(out, ', ')
end

-- the separate mods that are present; exists(path) -> true when the file is mounted
function M.duplicates(exists)
  local out = {}
  for _, name in ipairs(M.SEPARATE) do
    if exists('/mod_info/' .. name .. '/info.json') then out[#out + 1] = name end
  end
  return out
end

function M.message(list)
  return 'Wrench Complete already includes ' .. names(M.SEPARATE) .. '. Remove or disable the separate copies installed here (' .. names(list) .. ') and restart the game.'
end

-- the log line is written once when the extension loads; the on-screen message once when a level has started (the screen is not ready at load)
local logged, shown = false, false
local function duplicates()
  if not FS or not FS.fileExists then return {} end
  return M.duplicates(function(path) return FS:fileExists(path) end)
end

local function check(withMessage)
  local list = duplicates()
  if #list == 0 then return end
  local text = M.message(list)
  if not logged then logged = true log('E', 'wrench_complete', text) end
  if withMessage and not shown and ui_message then shown = true ui_message(text, 30, 'wrenchComplete') end
end

function M.onExtensionLoaded() pcall(check, false) end
function M.onClientPostStartMission() pcall(check, true) end

return M
