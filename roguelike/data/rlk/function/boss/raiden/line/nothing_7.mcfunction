title @a[tag=player] times 0 40 12
title @a[tag=player] subtitle {text:"그 무엇도 영원한 것은 없다.",color:"#d7b4ff",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 52
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ .45 1.18 0
execute as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.hit hostile @s ~ ~ ~ .8 0.97 0
execute as @a[tag=player] at @s run playsound minecraft:block.beacon.power_select hostile @s ~ ~ ~ .7 .5 0
execute as @a[tag=player] at @s run playsound minecraft:entity.lightning_bolt.thunder hostile @s ~ ~ ~ .55 .55 0
scoreboard players set #rdLine rd 0
