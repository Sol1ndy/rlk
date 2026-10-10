# 리롤: 이번 선택의 첫 번째는 무료, 그 뒤로 점점 비싸짐(lvup/rr_cost)
function rlk:lvup/rr_cost
execute if score @s gold < #pkRerollCost tmp run return run function rlk:lvup/act/reroll_deny
scoreboard players operation @s gold -= #pkRerollCost tmp
scoreboard players add @s pkRr 1
function rlk:lvup/roll
scoreboard players set @s pkRedraw 1
execute unless score #k348 snd matches 1 run function rlk:snd/f414
