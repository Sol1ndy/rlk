title @a[tag=player] times 0 10 0
title @a[tag=player] subtitle {text:"간파",color:"#bfe4ff",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 10
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ .45 0.62 0
execute as @a[tag=player] at @s run playsound minecraft:block.amethyst_block.hit hostile @s ~ ~ ~ .8 0.55 0
