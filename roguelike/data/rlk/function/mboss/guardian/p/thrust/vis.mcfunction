# hz_vis of the thrust lanes (@s = hazard marker, at it, rotated as it = the locked aim).
# #hzEv 0 create / 1 strike / 2 end; the decal parts carry the hazard id in mbHzI.
scoreboard players operation #gp1I mb = @s mbHzI
execute if score #hzEv mb matches 0 if score @s mbHzV matches 11 run function rlk:mboss/guardian/p/thrust/dk11
execute if score #hzEv mb matches 0 if score @s mbHzV matches 12 run function rlk:mboss/guardian/p/thrust/dk12
execute if score #hzEv mb matches 1 as @e[type=minecraft:block_display,tag=rlk_mb_gd_p1d] if score @s mbHzI = #gp1I mb run function rlk:mboss/guardian/p/thrust/dflash
execute if score #hzEv mb matches 2 as @e[type=minecraft:block_display,tag=rlk_mb_gd_p1d] if score @s mbHzI = #gp1I mb run kill @s
