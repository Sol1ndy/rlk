# A8 pattern tick 154.
function rlk:boss/scarlet/g/spot/d3
function rlk:mboss/mv/stop
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~3 ~ run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:5}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
function rlk:boss/scarlet/g/cut/aim {s:163}
