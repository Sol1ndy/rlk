# 3 heal orbs (any executor; the existing 회복구슬, #orbHealPct each): 6-14 b from the arena centre,
# 120 deg apart from a random bearing; the older ones go first (<= 3 alive).
kill @e[type=minecraft:item,tag=rlk_kn_orb]
execute store result score #t kn run random value 0..359
execute store result storage rlk:kn core.orb.a int 1 run scoreboard players get #t kn
execute store result storage rlk:kn core.orb.r double 0.1 run random value 60..140
function rlk:boss/arlecchino/bond/orb_at with storage rlk:kn core.orb
scoreboard players add #t kn 120
execute store result storage rlk:kn core.orb.a int 1 run scoreboard players get #t kn
execute store result storage rlk:kn core.orb.r double 0.1 run random value 60..140
function rlk:boss/arlecchino/bond/orb_at with storage rlk:kn core.orb
scoreboard players add #t kn 120
execute store result storage rlk:kn core.orb.a int 1 run scoreboard players get #t kn
execute store result storage rlk:kn core.orb.r double 0.1 run random value 60..140
function rlk:boss/arlecchino/bond/orb_at with storage rlk:kn core.orb
scoreboard players add #t kn 120
execute store result score #orbs kn if entity @e[type=minecraft:item,tag=rlk_kn_orb]
