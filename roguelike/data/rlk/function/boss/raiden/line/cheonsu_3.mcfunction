title @a[tag=player] times 0 30 12
title @a[tag=player] subtitle {text:"천수의 속박!",color:"#e6a3ff",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 42
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ .45 0.86 0
execute as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.hit hostile @s ~ ~ ~ .8 0.73 0
execute as @a[tag=player] at @s run playsound minecraft:block.beacon.power_select hostile @s ~ ~ ~ .7 .5 0
execute as @a[tag=player] at @s run playsound minecraft:entity.lightning_bolt.thunder hostile @s ~ ~ ~ .55 .55 0
scoreboard players set #rdLine rd 0
