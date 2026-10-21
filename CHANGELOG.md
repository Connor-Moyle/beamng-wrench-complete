# Changelog: Wrench Complete

## 0.10.8: Car Surface FX 0.4.9, Part Wear 0.1.1, Drivers 1.6.3 and Driver Injuries 0.2.2

For BeamNG 0.40. Wrench Works 1.8.6 and Street Legal 0.7.1 are as in 0.10.7. A pre-release for bug-checking.

- **Car Surface FX 0.4.9:** snow on the sides of a parked car is a faint dusting of soft flecks (it was hard white blobs) with the thick cap still on the roof, and slush thrown from the wheels is pale and translucent (both seen in the game). Real wall hits leave chips, scratches and crack-like lines at the place of the hit on metal panels (seen in the game; Panel damage is off by default: Mods > Car Surface FX > Crash). The dent shading on metal is gone (it read as dark blotches; dents come from the game's own physics). Belt-worn tyres throw 2 to 6 sparks per tick, and our spark code was seen to fire and to stay off with its switch off. Built, not yet tested in the game: what the sparks look like, the rubber marbles after a real burnout, cracks on plastic, fibreglass and carbon from a real hit, a pole hit, a side window breaking on other cars, and skid marks on dirt, gravel and snow.
- **Part Wear 0.1.1** (everything off by default: ESC > Mods > Part wear). Seen in the game: breakdowns (a shock absorber at 10 % blew after a roll, the engine at 14 % ran rough), worn paint through Car Surface FX (faded paint, grime, scuffs, rust spots), a worn clutch (a hard launch slips with it at 10 %), and a part swap in free roam sets back to new only the parts of the slot that changed. Rust on brake calipers and hubs changes the materials but nothing was visible. Built and tested offline only: the other breakdowns (soft brakes, a spring gone soft, the clutch's own message) and the finder fix for cars with 4-link front axles.
- **Drivers 1.6.3 and Driver Injuries 0.2.2:** one start warning fewer ("set new global variable: slrrInjuryCaps"). Seen in the game: a cold start without it; with both legs broken the pedal cap stayed in place and a respawn cleared it. Not seen: the broken-arm steering cap. The Drivers mod itself is unchanged.
- Known issues: Street Legal's Wet roads and walls is off by default; with it on, a heavy-rain crash can still happen at High graphics.

## 0.10.7: Wrench Works 1.8.6, Street Legal 0.7.1

For BeamNG 0.40. Wrench Works 1.8.6 and Street Legal 0.7.1 are the parts that changed; Drivers 1.6.2, Driver Injuries 0.2.1, Car Surface FX 0.4.8 and Part Wear 0.1.0 are as in 0.10.6. A pre-release for bug-checking.

- **Two start warnings fewer** in the game log: Street Legal 0.7.1 sets the drag extension's unload mode first (seen in the game: a cold start with the Street Legal 0.7.1 zip has no Street Legal warning or error), and Wrench Works 1.8.6 does the same for the pause menu's extension (tested offline; not yet seen in the game).
- Nothing else changed in the mods. Known issues: Street Legal's Wet roads and walls is off by default; with it on, a heavy-rain crash can still happen at High graphics. The log still shows other mods' start warnings and a new-global warning from Driver Injuries (a fix is being tested), none of them from this pack's other parts.

## 0.10.6: Street Legal 0.7.0, Car Surface FX 0.4.8

For BeamNG 0.40. Street Legal 0.7.0 and Car Surface FX 0.4.8 are the parts that changed; Wrench Works 1.8.5, Drivers 1.6.2, Driver Injuries 0.2.1 and Part Wear 0.1.0 are as in 0.10.5. A pre-release for bug-checking.

- **Street Legal 0.7.0: phone skins** (off by default: ESC > Mods > Street Legal > Screens and texts > Phone skin). Classic is the phone as it was; **Slate** is a modern look of our own, and you can add your own skins as folders in the user folder (see the Street Legal 0.7.0 notes). Seen in the game: both are listed, Slate shows on the phone and Classic is unchanged (an open phone changes the next time you open it).
- **Street Legal 0.7.0: Street Legal in free roam** (all off by default: ESC > Mods > Street Legal > Free roam). A master switch and one switch per feature (phone with the Maps and Cab apps, maps, map pins, weather, cab, car wash, dashboard); no career is started or saved and no money is spent. The weather, dashboard, phone and Map app were seen working at Low graphics; the big-map pins were not drawn in the test. Also in 0.7.0: a garage visit the career refuses says why on screen, and a billboard fallback (off by default, not yet seen in the game).
- **Car Surface FX 0.4.8:** every part has its own switch (Dust, Mud, Tyre rubber, Road grime, Tyre smoke, Sparks from belt-worn tyres) and a switched-off kind builds nothing (seen in the game); the Active features page lists the master switches of the test features. Belt-worn tyres keep their rubber tread (the game's metal flip had stopped the tyre force altogether), and the sparks come from our own code. The rubber heap lies between the rear wheels and stops near 400 g (seen with a test hook). Car Surface FX 0.4.6 and 0.4.7 are in it too (the ground marks cost less).
- Built, not yet tested in the game: how the tyre sparks look, the marbles' glow and smear and a real burnout, the metal dent look on red and white paint, a pole hit, carbon and fibreglass panels, mud spray trails, scuffs, grime on dark paint, a window breaking on other cars, and skid marks on dirt, gravel and snow at the new distance.
- Known issues: Street Legal's Wet roads and walls is off by default; with it on, a heavy-rain crash can still happen at High graphics. Street Legal prints one start warning about the drag extension's unload mode (harmless, fixed in the next Street Legal).

## 0.10.5: Car Surface FX 0.4.6 (the ground marks cost less)

For BeamNG 0.40. Car Surface FX 0.4.6 is the only part that changed (it includes 0.4.5); Wrench Works 1.8.5, Street Legal 0.6.1, Drivers 1.6.2, Driver Injuries 0.2.1 and Part Wear 0.1.0 are as in 0.10.4. A pre-release for bug-checking.

- **The skid and track marks take less time every frame.** With the marks full, the frame time standing still was 2.30 ms against 1.06 ms with marks off, and is 1.67 ms now; driving was 1.59 ms and is 1.52 ms (seen in the game). Skid marks still look continuous at 0, 20, 40 and 55 m and fade out towards 60 m (asphalt only). At most 300 marks are drawn at once (it was 800) and the draw distance is 60 m (it was 100); a saved setting with the old numbers moves to the new ones once, and a choice you make afterwards stays (Mods > Car Surface FX > Skid marks).
- **Dents on metal panels** (from 0.4.5; Panel damage is off by default: Mods > Car Surface FX > Crash, "Panel damage (test)"): a hit draws a dent with fewer paint chips where it was chips that read as dirt. Real hits leave marks and a reset that repairs the car takes them off (seen in the game).
- Built, not yet tested in the game: skid marks on dirt, gravel and snow at the new distance, a very fast camera turn (can leave a gap for up to a tenth of a second), how the dent reads on red and white paint, a side swipe, a pole hit, carbon and fibreglass panels, and marks after a recovery that keeps the damage.
- Street Legal's known issue is unchanged: Wet roads and walls is off by default since 0.6.1; with it on, a heavy-rain crash can still happen at High graphics.

## 0.10.4: Part Wear (new), Wrench Works 1.8.5, Drivers 1.6.2, Car Surface FX 0.4.4

For BeamNG 0.40. Street Legal 0.6.1 and Driver Injuries 0.2.1 are as in 0.10.3. Remove the separate Wrench Works, Street Legal, Drivers, Driver Injuries, Car Surface FX and Part Wear mods before installing this one. A pre-release for bug-checking.

- **New: Part Wear 0.1.0** (everything off by default; switch it on in ESC > Mods > Part wear). The parts of a car wear as you drive and a worn part changes the car. Seen in the game: worn brake pads brake later (about 1.5 times the stopping time with pads at 5 %), worn shock absorbers bounce more (4 bounces against 2), a worn engine is slower (7.8 s against 6.6 s from standstill to 20 m/s), worn metal and brake discs take rust and grime, wear stays with the car through a part swap, and the Wrench Works garage lists a worn part under Services with a price and repairs it. Built and tested offline only: springs, the clutch, breakdowns ("Parts can break"), the paint fade, and wear per career slot.
- **Wrench Works 1.8.5:** the driver look, Driver mode and pedestrian options are set only on the Pedestrians & Drivers page now (Wrench Works kept a second copy, which is what reset the helmet earlier). The garage's Drivers panel saves your pick there, and "No driver" there means no driver by default. A garage visit the career refuses says why on screen (1.8.4). Seen in the game: the garage panel's pick and outfit stay for a newly spawned car. Not yet seen: a click on the helmet on the Drivers page staying after a restart.
- **Drivers 1.6.2:** with Helmet on, the default drivers (Alison, Carla, Eric, Manuel) no longer get a pink "NO Mesh" label above the car (seen in the game); the helmet is added only to drivers whose model has one. Not yet checked: the helmet itself on the police officer and the racer.
- **Car Surface FX 0.4.4:** slush on snowy ground is pale grey-white (it read tan before) and melting snow takes the snow off the car and holds (both seen in the game). Built, not yet tested in the game: the mud spray trails, the rubber heap, scuffs, grime on dark paint, panel damage from a real hit, and a window breaking on other cars.
- Street Legal's known issue is unchanged: Wet roads and walls is off by default since 0.6.1; with it on, a heavy-rain crash can still happen at High graphics.

## 0.10.3: Car Surface FX 0.4.3

For BeamNG 0.40. Car Surface FX 0.4.3 is the only part that changed; Wrench Works 1.8.3, Street Legal 0.6.1, Drivers 1.6.1 and Driver Injuries 0.2.1 are as in 0.10.2. A pre-release for bug-checking.

- **Leak pools follow the volume let out:** a punctured radiator leaves one pool about 0.65 m across instead of an 8 cm spot, and a parked oil leak is one puddle again, not two.
- **Glass on asphalt** reads clearly, a **burnout** throws visible rubber chunks, and **snow** is lighter, with a clean white cap on the roof and boot lid.
- **Worn paint** keeps its wear on a respawn with the same config without doubling it; the tyres read the water film in heavy rain.
- **Built, not yet tested in the game** (see the Car Surface FX 0.4.3 notes): the rubber heap and the glow of hot rubber after a long burnout (the rubber marbles are off by default), the thin snow dusting on the sides, and the slush thrown from the wheels.
- The full list, with what is proven in the game and what is only built, is in the Car Surface FX v0.4.3 release notes.
- Street Legal's known issue is unchanged: Wet roads and walls is off by default since 0.6.1; with it on, a heavy-rain crash can still happen at High graphics.

## 0.10.2: Car Surface FX 0.4.1 (the mud is right again)

For BeamNG 0.40. Car Surface FX 0.4.1 is the only part that changed; Wrench Works 1.8.3, Street Legal 0.6.1, Drivers 1.6.1 and Driver Injuries 0.2.1 are as in 0.10.1. A pre-release for bug-checking.

- **Mud thrown from the tyres on dry loose ground reads as mud again.** Car Surface FX 0.4.0 shipped a tighter height cut that left only an even tan sand film; 0.4.1 has the dark ragged patches back, heaviest on the lower doors, the rear arch and the rear bumper. Use 0.10.2 instead of 0.10.1 or 0.10.0.
- Street Legal's known issue is unchanged: Wet roads and walls is off by default since 0.6.1; with it on, a heavy-rain crash can still happen at High graphics.

## 0.10.1: Street Legal 0.6.1 (wet roads and walls off by default)

Hotfix for 0.10.0, for BeamNG 0.40. Street Legal 0.6.1 is the only part that changed; Wrench Works 1.8.3, Drivers 1.6.1, Driver Injuries 0.2.1 and Car Surface FX 0.4.0 are as in 0.10.0. A pre-release for bug-checking.

- **Street Legal's "Wet roads and walls" is now off by default** and switched off once for everyone, because it is what crashes the graphics driver at High graphics in heavy rain on BeamNG 0.40. You can turn it back on in Mods > Street Legal (the row carries the warning).
- **Known issue:** with Wet roads and walls on, a heavy-rain crash can still happen at High graphics. With it off it was not seen (a 10-minute High-graphics heavy-rain test with it off, and puddles on, did not crash).
- Everything in the "not yet tested" list of 0.10.0 still applies.

## 0.10.0: Wrench Works 1.8.3, Street Legal 0.6.0, Drivers 1.6.1, Driver Injuries 0.2.1, Car Surface FX 0.4.0

For BeamNG 0.40. Remove the separate mods before installing this one. All five parts are the released versions, built from their tags. A pre-release for bug-checking.

### Known issue
- **At High graphics a heavy-rain crash can still happen** (the graphics driver stops), also with Street Legal 0.6.0's slower wet-road pace; it was not seen at Low graphics. Workaround: turn "Wet roads and walls" off (Mods > Street Legal), or lower the graphics quality in heavy rain.

### What is new
- **Active features** (Wrench Works 1.8.3): the first page of ESC > Mods lists every on/off switch of every part, grouped by mod. The driver's helmet, shirt and trouser colours and size you set in the Mods menu no longer reset when the game starts.
- **Parts of the game you can switch off** (Street Legal 0.6.0, Mods > Street Legal > Parts of the game, all on by default): spectators, sponsor billboards, ambient sounds, puddles, achievements, tips, markets, rally, races, clubs, crews, tow, taxi, jobs, and the bank, hospital, HUD phone pill, laptops, Maps and garage upgrades. A part that is off does nothing and loses its phone app; nothing is deleted.
- **Maps and the phone** (Street Legal): the Maps speed switch and the phone's K slide are on the Active features page; three presses of K now behave as three toggles.
- **Tyres keep their wear with the car** (Street Legal 0.6.0 with Car Surface FX 0.4.0, tyre simulation switched on); the swap to a different tyre part and the real Wrench Works garage fitting are not yet tested in the game.
- **Car Surface FX 0.4.0:** the tyre simulation (wear, heat, grip, smoke, debris, sparks, fire; off by default), mud and snow fixes, crash effects (debris, sparks, glass piles; off by default), and panel damage by part (off by default, not yet tested in the game).
- **Drivers & Pedestrians 1.6.1 and Driver Injuries 0.2.1:** their switches are on the Active features page; the pedestrian tab text no longer names a map; the steering-wheel read is more careful (built, not yet seen in the game).

### Not yet tested in the game
Panel damage by part, worn paint, the water film in heavy rain, the leak puddles with the new cap (glossy planes now off by default). See each part's own changelog for the full list.

### Street Legal 0.6.0 and the other parts
Their full notes are on their release pages: Wrench Works v1.8.3, Street Legal v0.6.0, Drivers v1.6.1 (with Injuries 0.2.1) and Car Surface FX v0.4.0.

## 0.9.2: Street Legal 0.5.2 (rain crash fix)

- **Crash fix:** on BeamNG 0.40, Street Legal's rain could crash the graphics driver when the wet world and puddles updated at the same time. They now take turns, and the wet world changes fewer materials per second. In our tests, a heavy-rain run that crashed every time before ran 8 minutes without a crash; tell us if you still see one.
- Wet tarmac (the darker road surface in rain) is now off by default and switched off once for everyone. Turn it back on in Mods > Street Legal. Turning it back on can still crash some graphics cards on 0.40.
- In a sudden downpour, puddles now appear gradually over the first half minute.
- **Known issue:** the crash fix was tested at Low graphics. At High graphics a heavy-rain crash has still been seen. Workaround: turn "Wet roads and walls" off, or lower the graphics quality.
- Everything else is unchanged from 0.9.1.

## 0.9.1: Wrench Works 1.8.2, for BeamNG 0.40

- Works with BeamNG 0.40. After a BeamNG update the game turns all mods off (its `disableModsAfterUpdate` setting): re-enable Wrench Complete in the Mods manager.
- Wrench Works 1.8.2 inside: **fixed** long drop-down lists in the Mods menu not saving your choice; **new** BeamNG 0.40 upscaling on the Graphics page (DLSS tested; FSR and XeSS are listed when your card supports them but are not tested yet).
- Street Legal 0.5.1, Drivers & Pedestrians 1.6.0, Driver Injuries 0.2.0 and Car Surface FX 0.3.0 are unchanged.

## 0.9.0: first combined release: Wrench Works 1.8.1, Street Legal 0.5.1, Drivers & Pedestrians 1.6.0, Driver Injuries 0.2.0, Car Surface FX 0.3.0

A pre-release for bug-checking. Version 1.0.0 follows after testing.

- One mod, one zip (`wrench_complete.zip`) instead of five. The garage, the career, the drivers, driver injuries and the car surface effects are all in it.
- The Valo City map is not included. Wrench Complete plays on West Coast USA.
- Remove the separate Wrench Works, Street Legal, Drivers & Pedestrians, Driver Injuries and Car Surface FX mods before installing: two copies clash.
- All settings are on one screen, **ESC > Mods**.
- After a BeamNG update the game turns all mods off (`disableModsAfterUpdate`): re-enable Wrench Complete in the Mods manager.
- The mod's scripts set each extension's unload mode before loading it, so BeamNG 0.40 no longer logs a warning for each one.

Included parts: Wrench Works (garage) 1.8.1, Street Legal (career) 0.5.1, Drivers & Pedestrians 1.6.0, Driver Injuries 0.2.0, Car Surface FX 0.3.0. Street Legal 0.5.1 fixes an error on the big map and a placeholder that showed in part names in the Part market.

Features that were built with offline tests and have had little play in the game yet are listed under **Known issues** in the README.
