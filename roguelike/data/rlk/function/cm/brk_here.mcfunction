# 실행 위치를 중심으로 수평 ±r, 세로 yl..yh 의 #rlk:cm_break 블록을 공기로. 진행 중인 런의 방 안쪽(벽 제외)만, y 201 이상만
execute unless score #active room matches 1 run return 0
summon minecraft:marker ~ ~ ~ {Tags:["rlk_cmbm"]}
execute store result score #bx tmp run data get entity @e[tag=rlk_cmbm,limit=1] Pos[0] 1000
execute store result score #by tmp run data get entity @e[tag=rlk_cmbm,limit=1] Pos[1] 1000
execute store result score #bz tmp run data get entity @e[tag=rlk_cmbm,limit=1] Pos[2] 1000
kill @e[tag=rlk_cmbm]
scoreboard players operation #bx tmp /= #1000 tmp
scoreboard players operation #by tmp /= #1000 tmp
scoreboard players operation #bz tmp /= #1000 tmp
$scoreboard players set #br tmp $(r)
$scoreboard players set #byl tmp $(yl)
$scoreboard players set #byh tmp $(yh)
scoreboard players operation #by0 tmp = #by tmp
scoreboard players operation #by0 tmp += #byl tmp
scoreboard players operation #by1 tmp = #by tmp
scoreboard players operation #by1 tmp += #byh tmp
execute if score #by0 tmp matches ..200 run scoreboard players set #by0 tmp 201
execute if score #by1 tmp < #by0 tmp run return 0
data modify storage rlk:cm zs set from storage rlk:room cur.zones
function rlk:cm/brk_z
