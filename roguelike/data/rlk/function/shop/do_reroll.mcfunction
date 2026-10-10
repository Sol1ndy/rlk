# @s = 플레이어. 리롤 비용 차감 + 모든 슬롯 재추첨
scoreboard players operation @s gold -= #rcost tmp
execute unless score #k167 snd matches 1 run function rlk:snd/f218
execute unless score #k2 snd matches 1 run function rlk:snd/f219
data modify storage rlk:pick picked set value []
data modify storage rlk:shop scan set from storage rlk:shop slots
function rlk:shop/reroll_loop
