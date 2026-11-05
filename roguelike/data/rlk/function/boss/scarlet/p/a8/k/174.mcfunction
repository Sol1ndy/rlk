# A8 pattern tick 174.
function rlk:boss/scarlet/rig_stub/look/blade/off
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=174},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run particle minecraft:dust{color:[0.88,0.25,0.62],scale:1.2} ~ ~ ~ 0.2 1.6 0.2 0 26 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=174},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1.5 0.23
