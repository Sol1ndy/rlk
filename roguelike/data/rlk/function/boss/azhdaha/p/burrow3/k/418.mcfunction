# burrow3 #azPT 418
function rlk:boss/azhdaha/px/normal
function rlk:boss/azhdaha/svc/floor_0
scoreboard players set #azBur mb 0
function rlk:boss/azhdaha/tr/done
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] if score @s mhpC matches ..1 run function rlk:boss/azhdaha/p/burrow3/last
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p23c]
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:boss/azhdaha/fx/p/dust
