# 두뇌가 없어진 리그(@s = 뿌리 부품, at @s): 같은 cmId 부품을 쓰러지는 모습으로, 몸 쪽을 보게 돌린 뒤 뒤로 날림
scoreboard players operation #did tmp = @s cmId
execute as @e[tag=rlk_c2pt,tag=!rlk_c2dying,distance=..6] if score @s cmId = #did tmp run tag @s add rlk_c2this
tag @e[tag=rlk_c2this] add rlk_c2dying
execute as @e[tag=rlk_c2this] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute as @e[tag=rlk_c2this,tag=rlk_c2glow] run data merge entity @s {Glowing:0b}
execute if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2this] run tp @s ~ ~ ~ ~ 0
scoreboard players set @s cmAD 0
scoreboard players set @s c2T2 0
execute if entity @s[tag=rlk_ns_pt] run function rlk:cm/ns/rig/die
execute if entity @s[tag=rlk_sl_pt] run function rlk:cm/sl/rig/die
execute if entity @s[tag=rlk_ss_pt] run function rlk:cm/ss/rig/die
execute if entity @s[tag=rlk_sp_pt] run function rlk:cm/sp/rig/die
execute if entity @s[tag=rlk_dr_pt] run function rlk:cm/dr/rig/die
execute unless score #c2kill snd matches 1 run function rlk:cm/c2/snd/kill
tag @e[tag=rlk_c2this] remove rlk_c2this
