# 장미탄 한 발 (위치·방향 = 총구): 0.5칸씩 12칸까지. 벽에서 멈추고, 적은 꿰뚫는다. 이 탄에 맞은 적 = rlk_np → 맞은 발수 nvHit +1
summon minecraft:marker ~ ~ ~ {Tags:["rlk_nvp"]}
tp @e[tag=rlk_nvp] ~ ~ ~ ~ ~
scoreboard players set #ps tmp 24
execute as @e[tag=rlk_nvp,limit=1] at @s run function rlk:char/navia/pellet
kill @e[tag=rlk_nvp]
scoreboard players add @e[tag=rlk_np] nvHit 1
tag @e[tag=rlk_np] remove rlk_np
