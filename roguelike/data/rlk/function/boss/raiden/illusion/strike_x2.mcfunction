# As the REAL illusion: the second diagonal stroke of its X.
function rlk:boss/raiden/illusion/pose {model:"illusion_wind"}
function rlk:boss/raiden/object_vfx/slash_xb
scoreboard players add #rdIlSlash rd 1
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.9 1.15 0.2
