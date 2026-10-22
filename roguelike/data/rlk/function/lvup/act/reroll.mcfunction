# 리롤: 이번 선택의 첫 번째는 무료, 그 뒤로는 주사위 하나씩(lvup/rr_cost). 주사위가 없으면 리롤할 수 없다
function rlk:lvup/rr_cost
execute unless score @s dice matches 0.. run scoreboard players set @s dice 0
execute if score @s dice < #pkRerollCost tmp run return run function rlk:lvup/act/reroll_deny
scoreboard players operation @s dice -= #pkRerollCost tmp
scoreboard players add @s pkRr 1
function rlk:lvup/roll
scoreboard players set @s pkRedraw 1
execute unless score #k348 snd matches 1 run function rlk:snd/f414
