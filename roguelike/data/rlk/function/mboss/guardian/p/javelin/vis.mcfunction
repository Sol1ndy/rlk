# hz_vis of the javelin lanes (@s = hazard marker, at it, rotated as it = the locked aim).
# #hzEv 0 create / 1 strike / 2 end; the decal parts carry the hazard id in mbHzI.
scoreboard players operation #gp2I mb = @s mbHzI
execute if score #hzEv mb matches 0 if score @s mbHzV matches 21 run function rlk:mboss/guardian/p/javelin/dk21
execute if score #hzEv mb matches 1 as @e[type=minecraft:block_display,tag=rlk_mb_gd_p2d] if score @s mbHzI = #gp2I mb run function rlk:mboss/guardian/p/javelin/dflash
execute if score #hzEv mb matches 2 as @e[type=minecraft:block_display,tag=rlk_mb_gd_p2d] if score @s mbHzI = #gp2I mb run kill @s
