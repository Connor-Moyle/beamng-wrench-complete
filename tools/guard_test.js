// Tests mod/lua/ge/extensions/wc_guard.lua outside the game: node tools/guard_test.js (needs fengari: NODE_PATH to a folder with it)
const path = require('path');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = require('fengari');
const L = lauxlib.luaL_newstate();
lualib.luaL_openlibs(L);
const dir = path.join(__dirname, '..', 'mod', 'lua', 'ge', 'extensions').split(path.sep).join('/');
const code = `
package.path = '${dir}/?.lua;' .. package.path
local G = require('wc_guard')
local function has(set) return function(p) return set[p] == true end end
assert(#G.duplicates(has({})) == 0, 'nothing separate: no warning')
local d = G.duplicates(has({ ['/mod_info/wrench_works/info.json'] = true, ['/mod_info/carSurfaceFx/info.json'] = true, ['/mod_info/wrench_complete/info.json'] = true }))
assert(#d == 2 and d[1] == 'wrench_works' and d[2] == 'carSurfaceFx', 'finds the separate copies, not Wrench Complete itself')
local m = G.message(d)
assert(m:find('Wrench Works, Car Surface FX', 1, true) and m:find('Drivers & Pedestrians', 1, true) and not m:find('wrench_works', 1, true) and m:find('Remove or disable', 1, true), 'the message names them as a player knows them')
local logged, shownCount = {}, 0
FS = { fileExists = function(_, p) return p == '/mod_info/street_legal/info.json' end }
log = function(level, tag, text) logged[#logged + 1] = level .. tag .. text end
ui_message = function() shownCount = shownCount + 1 end
G.onExtensionLoaded()
assert(#logged == 1 and shownCount == 0, 'at load: the log line only')
G.onClientPostStartMission() G.onClientPostStartMission()
assert(#logged == 1 and shownCount == 1, 'the message once at level start, the log line not repeated')
local G2 = package.loaded.wc_guard
FS = { fileExists = function() error('boom') end }
package.loaded.wc_guard = nil
local G3 = require('wc_guard')
assert(pcall(G3.onClientPostStartMission), 'an error inside never escapes')
return 'ok'
`;
if (lauxlib.luaL_dostring(L, to_luastring(code)) !== lua.LUA_OK) { console.error(to_jsstring(lua.lua_tostring(L, -1))); process.exit(1); }
console.log('wc_guard tests passed');
