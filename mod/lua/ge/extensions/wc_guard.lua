-- Wrench Complete: the five parts (Wrench Works, Street Legal, Drivers & Pedestrians, Driver Injuries, Car Surface FX) are inside this mod.
-- If a separate copy of one of them is also installed, its extensions would load twice: say so once, clearly, and write it to the log.
-- A separate copy shows as its own /mod_info/<name>/info.json in the mounted file system.

local M = {}

M.SEPARATE = { 'wrench_works', 'street_legal', 'slrr_drivers', 'slrr_injury', 'carSurfaceFx' }

-- the separate mods that are present; exists(path) -> true when the file is mounted
function M.duplicates(exists)
  local out = {}
  for _, name in ipairs(M.SEPARATE) do
    if exists('/mod_info/' .. name .. '/info.json') then out[#out + 1] = name end
  end
  return out
end

function M.message(list)
  return 'Wrench Complete already includes ' .. table.concat(M.SEPARATE, ', ') .. '. Remove or disable the separate copies installed here (' .. table.concat(list, ', ') .. ') and restart the game.'
end

local shown = false
local function check()
  if shown or not FS or not FS.fileExists then return end
  local list = M.duplicates(function(path) return FS:fileExists(path) end)
  if #list == 0 then return end
  shown = true
  local text = M.message(list)
  log('E', 'wrench_complete', text)
  if ui_message then ui_message(text, 30, 'wrenchComplete') end
end

function M.onClientPostStartMission() check() end
function M.onExtensionLoaded() check() end

return M
