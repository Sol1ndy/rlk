title @a[tag=player] times 0 7 0
title @a[tag=player] subtitle {text:"무념",color:"#e6a3ff",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 7
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ .3 1 0
