title @a[tag=player] times 0 22 12
title @a[tag=player] subtitle {text:"방해는 모두 베겠노라",color:"#e6a3ff",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 34
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ .45 0.94 0
execute as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.hit hostile @s ~ ~ ~ .8 0.79 0
execute as @a[tag=player] at @s run playsound minecraft:block.beacon.power_select hostile @s ~ ~ ~ .7 .5 0
scoreboard players set #rdLine rd 0
