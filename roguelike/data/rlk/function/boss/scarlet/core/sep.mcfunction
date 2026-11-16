# @s = the body; the avatar near her floor point. Round X's soft separation (body.py): inside 1.4 b (floor plane) the
# avatar goes straight away from her by what is missing, at most 0.25 b this tick (core/sep_push); within 1.75 b its
# Motion keeps no more pull toward her than leaves it 1.4 b off after this tick's physics (core/sep_motion). Not while
# the player is dead, reviving, choosing, in the map or held by a camera.
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if entity @a[tag=player,scores={vMap=1}] run return 0
execute if entity @a[tag=rlk_mb_camh] run return 0
scoreboard players set #mbPlG mb -1
execute unless function rlk:mboss/mv/plpos run return 0
execute store result score #bx_px hr run data get entity @s Pos[0] 1000
execute store result score #bx_pz hr run data get entity @s Pos[2] 1000
scoreboard players operation #bx_qx hr = #mbPX mb
scoreboard players operation #bx_qx hr -= #bx_px hr
scoreboard players operation #bx_qz hr = #mbPZ mb
scoreboard players operation #bx_qz hr -= #bx_pz hr
execute unless score #bx_qx hr matches -2500..2500 run return 0
execute unless score #bx_qz hr matches -2500..2500 run return 0
scoreboard players operation #bx_n hr = #bx_qx hr
scoreboard players operation #bx_n hr *= #bx_qx hr
scoreboard players operation #bx_k hr = #bx_qz hr
scoreboard players operation #bx_k hr *= #bx_qz hr
scoreboard players operation #bx_n hr += #bx_k hr
execute if score #bx_n hr matches 3062500.. run return 0
scoreboard players set #bx_d hr 0
execute if score #bx_n hr matches 400.. run function rlk:boss/scarlet/core/isqrt
execute if score #bx_n hr matches 400.. run scoreboard players operation #bx_d hr = #bx_r hr
execute if score #bx_d hr matches ..9 run return run function rlk:boss/scarlet/core/sep_face
scoreboard players operation #bx_ux hr = #bx_qx hr
scoreboard players operation #bx_ux hr *= #c1000 hr
scoreboard players operation #bx_ux hr /= #bx_d hr
scoreboard players operation #bx_uz hr = #bx_qz hr
scoreboard players operation #bx_uz hr *= #c1000 hr
scoreboard players operation #bx_uz hr /= #bx_d hr
function rlk:boss/scarlet/core/sep_go
