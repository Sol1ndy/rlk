# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg known). Flags and scores only.
# Element record (K5): during the guard window, a hit with #elem 1-4 (reaction damage #tfm excluded)
# counts once per element per 8 t; 3 hits record a new element, 9 re-record slot A's.
scoreboard players set #gdFlash mb 1
execute unless score #gdRecOn mb matches 1 run return 0
execute if score #gdRecNew mb matches 1.. run return 0
execute if score #tfm tmp matches 1 run return 0
execute if score #elem tmp matches 1 run return run function rlk:mboss/guardian/rec/e1
execute if score #elem tmp matches 2 run return run function rlk:mboss/guardian/rec/e2
execute if score #elem tmp matches 3 run return run function rlk:mboss/guardian/rec/e3
execute if score #elem tmp matches 4 run return run function rlk:mboss/guardian/rec/e4
