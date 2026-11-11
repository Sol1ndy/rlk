# A8 fail (#gres 2 at T + 220; not lethal: ULT60_LETHAL False; @s = the body): the dive lands on the
# player: ult/fail60 at the player's floor spot (500 per mille, never kills, the push ring there blows them
# ~3 b off it); she lands on the impact point (from 1 b above it in 2 t), g_reform.
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/scarlet/ult/fail60
function rlk:boss/scarlet/rig/play/g_reform
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/land
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
