# Changelog: Wrench Complete

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
