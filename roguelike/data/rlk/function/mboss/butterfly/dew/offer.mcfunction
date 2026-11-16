# The groggy's #bfDew1 달빛 이슬 (1 or 2, opposite each other): they stay until taken, the next transformation's
# sphere or the next butterfly form's end; #bfDew1 = the orbs still offered (a /reload brings them back, fix S4).
execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dew] at @s run particle minecraft:poof ~ ~ ~ 0.2 0.2 0.2 0.02 6 force @a[tag=player]
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_dew]
scoreboard players set #bfDewN mb 0
scoreboard players set #bfDewP mb 0
execute store result score #bfX mb run random value 0..359
function rlk:mboss/butterfly/dew/one
scoreboard players add #bfX mb 180
execute if score #bfDew1 mb matches 2.. run function rlk:mboss/butterfly/dew/one
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
