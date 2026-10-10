# @s = 플레이어. 최대 체력의 #orbHealPct% 회복 (최소 1)
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #orbHealPct tmp
scoreboard players operation #heal tmp /= #100 tmp
# 붉은 약초: 회복량 증가
execute if score @s it_red_herb matches 1.. run function rlk:items/proc/herb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
execute unless score #k30 snd matches 1 run function rlk:snd/f32
