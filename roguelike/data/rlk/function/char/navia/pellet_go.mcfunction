# 장미탄 한 발 (위치·방향 = 총구): 0.5칸씩 12칸까지. 벽에서 멈추고, 적은 꿰뚫는다. 이 탄에 맞은 적 = rlk_np → 맞은 발수 nvHit +1
summon minecraft:marker ~ ~ ~ {Tags:["rlk_nvp"]}
tp @e[tag=rlk_nvp] ~ ~ ~ ~ ~
scoreboard players set #ps tmp 24
execute as @e[tag=rlk_nvp,limit=1] at @s run function rlk:char/navia/pellet
kill @e[tag=rlk_nvp]
# 챕터 보스 히트 프록시(rlk_mb_px)에 맞은 탄 = 몸체에 맞은 탄(몸체는 한 번만 셈, 프록시는 셈하지 않음)
execute if entity @e[tag=rlk_np,tag=rlk_mb_px,limit=1] run tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] add rlk_np
tag @e[tag=rlk_np,tag=rlk_mb_px] remove rlk_np
scoreboard players add @e[tag=rlk_np] nvHit 1
tag @e[tag=rlk_np] remove rlk_np
