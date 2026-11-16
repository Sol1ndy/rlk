# 두뇌가 없어진 리그(@s = 뿌리 부품, at @s): 같은 cmId 부품을 쓰러지는 모습으로, 몸 쪽을 보게 돌린 뒤 뒤로 날림
scoreboard players operation #did tmp = @s cmId
execute as @e[tag=rlk_c3pt,tag=!rlk_c3dying,distance=..6] if score @s cmId = #did tmp run tag @s add rlk_c3this
tag @e[tag=rlk_c3this] add rlk_c3dying
execute as @e[tag=rlk_c3this] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute as @e[tag=rlk_c3this,tag=rlk_c3glow] run data merge entity @s {Glowing:0b}
execute if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c3this] run tp @s ~ ~ ~ ~ 0
scoreboard players set @s cmAD 0
scoreboard players set @s c2T2 0
execute if entity @s[tag=rlk_fu_pt] run function rlk:cm/fu/rig/die
execute if entity @s[tag=rlk_em_pt] run function rlk:cm/em/rig/die
execute if entity @s[tag=rlk_sb_pt] run function rlk:cm/sb/rig/die
execute if entity @s[tag=rlk_cw_pt] run function rlk:cm/cw/rig/die
execute unless score #c3kill snd matches 1 run function rlk:cm/c3/snd/kill
tag @e[tag=rlk_c3this] remove rlk_c3this
