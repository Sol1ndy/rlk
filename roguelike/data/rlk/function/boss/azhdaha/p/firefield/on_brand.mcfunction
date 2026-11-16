# Rule 33 (plan 4.7; s2.md 9): a Pyro brand by a strike hit, as the body at the player's floor point (#azBrNew 1 new /
# 0 refresh): a fire field r 4.5 / 160 t here, or the first fire field within 4 b
# is extended instead (fld/refresh: at most 2x its base life). Fire-rule fields ignore the clear melee points.
scoreboard players set #aq33X mb 0
execute if score #aq33X mb matches 0 if score #azF0 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld0,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF1 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld1,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF2 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld2,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF3 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld3,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF4 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld4,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF5 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld5,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF6 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld6,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
execute if score #aq33X mb matches 0 if score #azF7 mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_fld7,distance=..4,limit=1] run function rlk:boss/azhdaha/p/firefield/ext
# (FIX FAIR-22) a new field at most every 100 t (#aq33C = the module tick it may come again); extending stays
execute if score #aq33X mb matches 0 unless score #aq33C mb > #azClk mb run function rlk:boss/azhdaha/p/firefield/arm
function rlk:boss/azhdaha/p/firefield/amb_on
