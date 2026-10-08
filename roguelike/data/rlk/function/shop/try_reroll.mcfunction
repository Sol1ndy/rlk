# @s = 플레이어. 리롤 비용 확인 후 전체 리롤/거절
execute unless score @s gold matches 0.. run scoreboard players set @s gold 0
execute store result score #rcost tmp run data get storage rlk:shop reroll_cost
execute if score @s gold >= #rcost tmp run function rlk:shop/do_reroll
execute unless score @s gold >= #rcost tmp run function rlk:shop/deny
