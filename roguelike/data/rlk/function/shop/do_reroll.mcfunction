# @s = 플레이어. 리롤 비용 차감 + 모든 슬롯 재추첨
scoreboard players operation @s gold -= #rcost tmp
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 0.8 1.2
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.4 1.6
data modify storage rlk:pick picked set value []
data modify storage rlk:shop scan set from storage rlk:shop slots
function rlk:shop/reroll_loop
