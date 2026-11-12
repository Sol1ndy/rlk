# @s = the anchor: 1 when the player body is within 1.0 b horizontal and |dy| < 1.5 b of it (positions x100), else fail.
execute store result score #riftBx room run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #riftBy room run data get entity @e[tag=rlk_body,limit=1] Pos[1] 100
execute store result score #riftBz room run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
scoreboard players operation #riftBx room -= @s riftX
scoreboard players operation #riftBy room -= @s riftY
scoreboard players operation #riftBz room -= @s riftZ
execute unless score #riftBy room matches -149..149 run return fail
execute unless score #riftBx room matches -100..100 run return fail
execute unless score #riftBz room matches -100..100 run return fail
scoreboard players operation #riftBx room *= #riftBx room
scoreboard players operation #riftBz room *= #riftBz room
scoreboard players operation #riftBx room += #riftBz room
execute if score #riftBx room matches 10001.. run return fail
return 1
