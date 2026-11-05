# A13 pattern tick 200.
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.3 0.3 0.3 0 10 force @a[tag=player]
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:8}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute at @s run playsound minecraft:block.grass.step hostile @a[tag=player] ~ ~ ~ 0.3 1 0.1
function rlk:boss/scarlet/g/cut/aim {s:211}
