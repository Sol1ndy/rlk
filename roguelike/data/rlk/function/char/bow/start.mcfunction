# 조준 시작 (@s = 플레이어). bowT = 당긴 틱 수. 손에 든 활 모양은 char/bow/charge_tick 이 바꾼다
scoreboard players set @s bowT 1
scoreboard players set @s bowK 0
scoreboard players set @s bowSt 0
scoreboard players set @s bowPm -1
# 1인칭: 조준 중 느려짐(숄더뷰는 view/move 가 #bowSlow 로 처리)
attribute @s minecraft:movement_speed modifier remove rlk:bow_aim
execute if entity @s[tag=rlk_body] run attribute @s minecraft:movement_speed modifier add rlk:bow_aim -0.6 add_multiplied_total
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:item.crossbow.loading_start master @a ~ ~ ~ 0.6 1.2
