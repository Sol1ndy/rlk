# @s = round 4's player circle: toward the centre by <= 5 b but never nearer than 8 b to it (the
# emergence spot); a player inside 8 b gets it pushed out to 8 b.
scoreboard players set #aq42N mb 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..8,limit=1] run return run function rlk:mboss/azhdaha/p/bolt/r4_out
execute at @s run function rlk:mboss/azhdaha/p/bolt/r4_in
function rlk:mboss/azhdaha/u/clamp_r {r:24}
