# Changelog: Wrench Complete

## 0.9.2: Street Legal 0.5.2 (rain crash fix)

- **Crash fix:** on BeamNG 0.40, Street Legal's rain could crash the graphics driver when the wet world and puddles updated at the same time. They now take turns, and the wet world changes fewer materials per second. In our tests, a heavy-rain run that crashed every time before ran 8 minutes without a crash; tell us if you still see one.
- Wet tarmac (the darker road surface in rain) is now off by default and switched off once for everyone. Turn it back on in Mods > Street Legal. Turning it back on can still crash some graphics cards on 0.40.
- In a sudden downpour, puddles now appear gradually over the first half minute.
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
