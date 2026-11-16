# 쓰러지는 리그 한 틱 (@s = 뿌리, at @s). 1~6틱: 뒤로 0.32칸씩(앞이 비었을 때만) · 포물선(올라간 만큼만 내려옴 → 처음 높이 아래로는 안 감), 8틱: 터짐
scoreboard players add @s cmAD 1
scoreboard players operation #did tmp = @s cmId
execute as @e[tag=rlk_c2dying,distance=..6] if score @s cmId = #did tmp run tag @s add rlk_c2this
scoreboard players set #c2ok tmp 0
execute if score @s cmAD matches 1..6 positioned ^ ^ ^-0.32 if block ~ ~0.2 ~ #rlk:cm_pass if block ~ ~1.2 ~ #rlk:cm_pass run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ^ ^ ^-0.32
execute if score @s cmAD matches 1 if block ~ ~2.4 ~ #rlk:cm_pass as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~0.26 ~
execute if score @s cmAD matches 1 if block ~ ~2.4 ~ #rlk:cm_pass run scoreboard players add @s c2T2 26
execute if score @s cmAD matches 2 if block ~ ~2.4 ~ #rlk:cm_pass as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~0.16 ~
execute if score @s cmAD matches 2 if block ~ ~2.4 ~ #rlk:cm_pass run scoreboard players add @s c2T2 16
execute if score @s cmAD matches 3 if block ~ ~2.4 ~ #rlk:cm_pass as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~0.06 ~
execute if score @s cmAD matches 3 if block ~ ~2.4 ~ #rlk:cm_pass run scoreboard players add @s c2T2 6
execute if score @s cmAD matches 4 if score @s c2T2 matches 6.. as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~-0.06 ~
execute if score @s cmAD matches 4 if score @s c2T2 matches 6.. run scoreboard players remove @s c2T2 6
execute if score @s cmAD matches 5 if score @s c2T2 matches 16.. as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~-0.16 ~
execute if score @s cmAD matches 5 if score @s c2T2 matches 16.. run scoreboard players remove @s c2T2 16
execute if score @s cmAD matches 6 if score @s c2T2 matches 26.. as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~-0.26 ~
execute if score @s cmAD matches 6 if score @s c2T2 matches 26.. run scoreboard players remove @s c2T2 26
execute if score @s cmAD matches 3 if entity @s[tag=rlk_ns_pt] run function rlk:cm/ns/rig/fling
execute if score @s cmAD matches 3 if entity @s[tag=rlk_sl_pt] run function rlk:cm/sl/rig/fling
execute if score @s cmAD matches 3 if entity @s[tag=rlk_ss_pt] run function rlk:cm/ss/rig/fling
execute if score @s cmAD matches 3 if entity @s[tag=rlk_sp_pt] run function rlk:cm/sp/rig/fling
execute if score @s cmAD matches 3 if entity @s[tag=rlk_dr_pt] run function rlk:cm/dr/rig/fling
execute if score @s cmAD matches 8.. run function rlk:cm/c2/pop
tag @e[tag=rlk_c2this] remove rlk_c2this
