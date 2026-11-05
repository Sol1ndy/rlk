# R1 pattern tick 20.
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.95 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.3 0.4 0.3 0 12 force @a[tag=player]
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
function rlk:boss/scarlet/g/cut/lock {s:27}
