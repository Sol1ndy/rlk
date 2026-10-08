# 당기는 중 (@s = 플레이어, at 몸). bowT = 조준을 시작한 뒤 흐른 틱. 쏘는 것은 좌클릭(combat/on_attack → char/bow/release)
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run return run function rlk:char/bow/cancel
execute if score @s dead matches 1 run return run function rlk:char/bow/cancel
execute if score @s pkMode matches 1.. run return run function rlk:char/bow/cancel
scoreboard players add @s bowT 1
scoreboard players operation #ct tmp = @s bowT
execute if score #ct tmp >= #bowT1 tmp unless score @s bowSt matches 1.. run function rlk:char/bow/stage1
execute if score #charN tmp matches 2 if score @s bowSt matches 1.. run function rlk:char/yoimiya/charge_tick
# 활 모양(리소스팩의 당긴 활 모델): 아바타 3단계 / 손에 든 활 2단계
scoreboard players set #pm tmp 0
execute if score #ct tmp matches 7.. run scoreboard players set #pm tmp 1
execute if score #ct tmp matches 14.. run scoreboard players set #pm tmp 2
execute unless score #pm tmp = @s bowPm run function rlk:char/bow/hand_pull
execute unless score #pm tmp = @s bowPm if entity @e[tag=rlk_av,limit=1] run function rlk:char/bow/av_pull
scoreboard players operation @s bowPm = #pm tmp
execute if score @s bowSt matches 1.. anchored eyes run particle minecraft:small_flame ^-0.3 ^-0.25 ^0.9 0.05 0.05 0.05 0.005 1
