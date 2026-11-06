# tail3 #apq34T 0
function rlk:boss/apep/play/tail_p3
execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p34","rlk_mb_ap_p34f"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p34f,limit=1] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players operation #apq34H mb = #mbHitEv mb
