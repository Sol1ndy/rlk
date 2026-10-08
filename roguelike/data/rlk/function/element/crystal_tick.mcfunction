# @s = 결정 조각, at @s
scoreboard players remove @s life 1
particle minecraft:wax_on ~ ~0.3 ~ 0.12 0.12 0.12 0 1
execute if score @s life matches ..0 run return run kill @s
execute unless entity @e[tag=rlk_body,distance=..1.6] run return 0
scoreboard players operation #amt tmp = @s rxDmg
# 각인 반석: 방어막량 증가 / 그 원소 피해 증가
execute if score petra engN matches 2.. run function rlk:engravings/petra/pick
execute as @a[tag=player,limit=1] run function rlk:element/shield_gain
# 로노바: 공허 결정 = 공허 잔향
execute if entity @s[tag=rlk_rncr] if score #charN tmp matches 7 as @a[tag=player,limit=1] run function rlk:char/ronova/cr_pick
# 나비아: 결정 조각을 주우면 결정 파편 +1
execute if score #charN tmp matches 6 as @a[tag=player,limit=1] run function rlk:char/navia/shard_gain
kill @s
