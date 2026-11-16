# @s = the body gliding (rlk_mb_mv): the step mboss/mv/tick takes next tick (its own arithmetic at mbMvT + 1) against the
# avatar now. A step that would come nearer than 1.6 b to it: core/guard_stop (she stops on her path). A leap (mbMvH):
# its end only (core/guard_arc). Centi-blocks relative to her: every product stays inside int32.
execute at @s positioned ~ 201 ~ unless entity @e[tag=rlk_body,distance=..11] run return 0
execute if score @s mbMvH matches 1.. run return run function rlk:boss/scarlet/core/guard_arc
scoreboard players set #mbPlG mb -1
execute unless function rlk:mboss/mv/plpos run return 0
execute store result score #bx_px hr run data get entity @s Pos[0] 1000
execute store result score #bx_pz hr run data get entity @s Pos[2] 1000
scoreboard players operation #bx_t hr = @s mbMvT
scoreboard players add #bx_t hr 1
scoreboard players operation #bx_nx hr = @s mbMvX1
scoreboard players operation #bx_nx hr -= @s mbMvX0
scoreboard players operation #bx_nx hr *= #bx_t hr
scoreboard players operation #bx_nx hr /= @s mbMvN
scoreboard players operation #bx_nx hr += @s mbMvX0
scoreboard players operation #bx_nz hr = @s mbMvZ1
scoreboard players operation #bx_nz hr -= @s mbMvZ0
scoreboard players operation #bx_nz hr *= #bx_t hr
scoreboard players operation #bx_nz hr /= @s mbMvN
scoreboard players operation #bx_nz hr += @s mbMvZ0
scoreboard players operation #bx_dx hr = #bx_nx hr
scoreboard players operation #bx_dx hr -= #bx_px hr
scoreboard players operation #bx_dx hr /= #c10 hr
scoreboard players operation #bx_dz hr = #bx_nz hr
scoreboard players operation #bx_dz hr -= #bx_pz hr
scoreboard players operation #bx_dz hr /= #c10 hr
scoreboard players operation #bx_qx hr = #mbPX mb
scoreboard players operation #bx_qx hr -= #bx_px hr
scoreboard players operation #bx_qx hr /= #c10 hr
scoreboard players operation #bx_qz hr = #mbPZ mb
scoreboard players operation #bx_qz hr -= #bx_pz hr
scoreboard players operation #bx_qz hr /= #c10 hr
scoreboard players operation #bx_a hr = #bx_dx hr
scoreboard players operation #bx_a hr *= #bx_dx hr
scoreboard players operation #bx_k hr = #bx_dz hr
scoreboard players operation #bx_k hr *= #bx_dz hr
scoreboard players operation #bx_a hr += #bx_k hr
execute if score #bx_a hr matches ..0 run return 0
scoreboard players operation #bx_b hr = #bx_qx hr
scoreboard players operation #bx_b hr *= #bx_dx hr
scoreboard players operation #bx_k hr = #bx_qz hr
scoreboard players operation #bx_k hr *= #bx_dz hr
scoreboard players operation #bx_b hr += #bx_k hr
execute if score #bx_b hr matches ..0 run return 0
scoreboard players operation #bx_u hr = #bx_b hr
scoreboard players operation #bx_u hr *= #c1000 hr
scoreboard players operation #bx_u hr /= #bx_a hr
execute if score #bx_u hr matches 1001.. run scoreboard players set #bx_u hr 1000
scoreboard players operation #bx_k hr = #bx_dx hr
scoreboard players operation #bx_k hr *= #bx_u hr
scoreboard players operation #bx_k hr /= #c1000 hr
scoreboard players operation #bx_qx hr -= #bx_k hr
scoreboard players operation #bx_k hr = #bx_dz hr
scoreboard players operation #bx_k hr *= #bx_u hr
scoreboard players operation #bx_k hr /= #c1000 hr
scoreboard players operation #bx_qz hr -= #bx_k hr
scoreboard players operation #bx_h hr = #bx_qx hr
scoreboard players operation #bx_h hr *= #bx_qx hr
scoreboard players operation #bx_k hr = #bx_qz hr
scoreboard players operation #bx_k hr *= #bx_qz hr
scoreboard players operation #bx_h hr += #bx_k hr
execute if score #bx_h hr matches 25600.. run return 0
function rlk:boss/scarlet/core/guard_stop
