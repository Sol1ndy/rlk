scoreboard players operation @s skShown = #sk tmp
clear @s *[minecraft:custom_data~{rlk_ui:{role:"skill"}}]
data modify storage rlk:chars it set from storage rlk:chars cur.skill
execute store result storage rlk:chars it.n int 1 run scoreboard players get #sk tmp
execute if score #sk tmp matches 0 run function rlk:char/skill_item_ready with storage rlk:chars it
execute if score #sk tmp matches 1.. run function rlk:char/skill_item_cd with storage rlk:chars it
execute if score #sk tmp matches -1 run function rlk:char/skill_item_active with storage rlk:chars it
scoreboard players set #skn tmp -10
scoreboard players operation #skn tmp -= #sk tmp
execute if score #sk tmp matches ..-11 store result storage rlk:chars it.n int 1 run scoreboard players get #skn tmp
execute if score #sk tmp matches ..-11 run function rlk:char/skill_item_ready_n with storage rlk:chars it
