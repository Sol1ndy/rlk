# The 중간보스 gate object was clicked (@s = its rlk_obj marker, at @s; room/obj/click already refuses
# clicks during combat). Starts the zone fight; room/mob_wave calls mboss/start 1.5 s later.
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @a[tag=player] [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"난이도가 '평화로움'이면 중간보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 누르세요.",color:"gray",bold:false}]
execute unless entity @e[tag=rlk_zone,scores={zkind=15,zst=3},limit=1] run return 0
execute if entity @e[tag=rlk_mb_body,limit=1] run return 0
execute unless data storage rlk:mboss cur run function rlk:mboss/roll
execute unless data storage rlk:mboss cur run return 0
function rlk:room/obj/kill_group
execute as @e[tag=rlk_zone,scores={zkind=15,zst=3},sort=nearest,limit=1] at @s run function rlk:room/combat_start
scoreboard players set #spawnT room 30
title @a[tag=player] times 6 46 14
title @a[tag=player] subtitle {nbt:"cur.sub",storage:"rlk:mboss",color:"#E8E2D0"}
title @a[tag=player] title {nbt:"cur.title",storage:"rlk:mboss",interpret:true}
scoreboard players set @a[tag=player] vBig 66
scoreboard players set @a[tag=player] ttlT 66
execute as @a[tag=player] at @s run playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 0.7 0.6
execute as @a[tag=player] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.7
