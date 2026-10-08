# 핏값이 새겨지는 순간 (@s = 맞은 몹, at 몸통): 플레이어에게서 날아온 핏빛 줄기 + 큰 X자
tag @s add rlk_arS
scoreboard players set #sn tmp 0
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ facing entity @s eyes run function rlk:char/arlecchino/streak
tag @s remove rlk_arS
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.75 ^-0.75 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.75 ^0.75 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.60 ^-0.60 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.60 ^0.60 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.45 ^-0.45 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.45 ^0.45 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.30 ^-0.30 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.30 ^0.30 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.15 ^-0.15 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^-0.15 ^0.15 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.00 ^0.00 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.00 ^-0.00 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.15 ^0.15 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.15 ^-0.15 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.30 ^0.30 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.30 ^-0.30 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.45 ^0.45 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.45 ^-0.45 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.60 ^0.60 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.60 ^-0.60 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.75 ^0.75 ^0.5 0 0 0 0 1
execute positioned ~ ~1 ~ facing entity @a[tag=player,limit=1] eyes run particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.4} ^0.75 ^-0.75 ^0.5 0 0 0 0 1
particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.04 8
playsound minecraft:entity.player.attack.crit master @a ~ ~ ~ 0.5 0.6
