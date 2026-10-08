# @s = 플레이어 (매 틱). #shK = 지금 보여 줄 보호막 종류: 0 없음 / 1 방어막(결정·아이템, shieldHP — 금빛) / 2 각인 수호의 보호막(gShield — 푸른빛)
scoreboard players set #shK view 0
execute if score @s gShield matches 1.. run scoreboard players set #shK view 2
execute if score @s shieldHP matches 1.. run scoreboard players set #shK view 1
execute unless entity @e[tag=rlk_av,limit=1] run scoreboard players set #shK view 0
execute if score @s dead matches 1 run scoreboard players set #shK view 0
# 사라짐
execute if score #shK view matches 0 if entity @e[tag=rlk_shfx,limit=1] run function rlk:view/shield_off
execute if score #shK view matches 0 run return 0
# 종류가 바뀌면 색이 다른 것으로 다시 만든다 / 없으면 만든다
execute if entity @e[tag=rlk_shfx,limit=1] unless score #shK view = #shPrev view run kill @e[tag=rlk_shfx]
execute unless entity @e[tag=rlk_shfx,limit=1] at @e[tag=rlk_av,limit=1] run function rlk:view/shield_on
scoreboard players operation #shPrev view = #shK view
# 아바타를 따라다니며 돈다: 울타리는 천천히, 바깥의 조각들은 반대로 조금 빠르게
execute as @e[tag=rlk_shfx,tag=!rlk_shorb] at @e[tag=rlk_av,limit=1] rotated as @s run tp @s ~ ~ ~ ~4 0
execute as @e[tag=rlk_shorb] at @e[tag=rlk_av,limit=1] rotated as @s run tp @s ~ ~ ~ ~-9 0
# 가끔 반짝임
scoreboard players add #shTk view 1
execute if score #shTk view matches 8.. run scoreboard players set #shTk view 0
execute if score #shTk view matches 0 at @e[tag=rlk_av,limit=1] run particle minecraft:end_rod ~ ~0.4 ~ 0.6 0.2 0.6 0.005 1
