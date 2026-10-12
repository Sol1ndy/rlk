title @a[tag=player] times 0 22 12
title @a[tag=player] subtitle {text:"뇌전은 인간의 의지 따위로 변하지 않아",color:"#d7b4ff",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 34
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ .45 1.34 0
execute as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.hit hostile @s ~ ~ ~ .8 1.09 0
execute as @a[tag=player] at @s run playsound minecraft:block.beacon.power_select hostile @s ~ ~ ~ .7 .5 0
scoreboard players set #rdLine rd 0
