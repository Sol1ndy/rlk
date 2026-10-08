# @s = 반응이 일어난 몹. 씨앗이 붙어 있으면 다음 처리 때 모든 씨앗에 피해(예약)
execute store result score #now itv run time query gametime
execute unless score @s skEnd > #now itv run return 0
scoreboard players operation #skCd itv = #skCdT tmp
summon minecraft:marker ~ ~ ~ {Tags:["rlk_iq","rlk_iqn"]}
scoreboard players set @e[tag=rlk_iqn] iqK 1
tag @e[tag=rlk_iqn] remove rlk_iqn
