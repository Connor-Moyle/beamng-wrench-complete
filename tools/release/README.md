# Release script

`release.py --merged wrench_complete` builds `wrench_complete.zip` from the released tags of the five parts (Wrench Works, Street Legal, Drivers & Pedestrians, Driver Injuries, Car Surface FX), refuses on any file path two parts both ship with different content, leaves out the Valo City map and the development files, and runs `clean_install_test.py --single` on the result.

The source repositories and their tags are listed in `release.json` (the `src` and `pin` of each mod). Paths in it are those of the maintainer's machine: change them to build elsewhere.
