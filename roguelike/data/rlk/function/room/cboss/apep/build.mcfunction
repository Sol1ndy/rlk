# GENERATED: @s = a zone marker of the apep entrance (room/zone_build): its blocks; the entrance zone then runs
# the chapter prep at itself (mboss/cb/prep: cprep, the arena forceload and sliced build, the module prep).
execute if score @s zid matches 1 run function rlk:room/cboss/apep/z1
execute if score @s zid matches 2 run function rlk:room/cboss/apep/z2
execute if score @s zid matches 2 at @s run function rlk:mboss/cb/prep
