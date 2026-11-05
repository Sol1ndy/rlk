# A8 pattern tick 49.
execute at @s run playsound minecraft:entity.breeze.jump hostile @a[tag=player] ~ ~ ~ 0.4 1 0.13
function rlk:boss/scarlet/g/spot/over
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~2.5 ~ run function rlk:mboss/mv/leap {t:6,h:30}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
