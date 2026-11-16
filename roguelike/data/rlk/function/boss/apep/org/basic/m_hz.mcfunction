# The O1 cone at the floor point, rotated at the Heart (quiet: no decal, the lean is the tell).
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute if entity @s[tag=rlk_mb_ap_buff] run return run function rlk:mboss/hz/sector {r:31,a:27,tell:10,dmg:30}
function rlk:mboss/hz/sector {r:31,a:27,tell:10,dmg:25}
