# A8 fail (#gres 2 at T + 220; not lethal: ULT60_LETHAL False; @s = the body): the dive lands on the
# player: ult/fail60 at the player's floor spot (500 per mille, never kills); round X (x_brief cause 6): her
# landing point first (g/spot/land, 2 b from the player), the push ring centred THERE (ult/fail60_push: straight away
# from her to 5 b; it was centred on the player and sent them toward the arena start, through her when
# they faced it); she lands there (from 1 b above it in 2 t), g_reform.
function rlk:boss/scarlet/g/spot/land
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/scarlet/ult/fail60
execute at @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:boss/scarlet/ult/fail60_push
function rlk:boss/scarlet/rig/play/g_reform
function rlk:mboss/mv/face
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
