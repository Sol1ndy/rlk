# sink_p3 (20 t)
execute if score @s apRigT matches 2 run function rlk:mboss/apep/rig_stub/hands/p3_curl
execute if score @s apRigT matches 6 run function rlk:mboss/apep/rig_stub/look/face/hidden
execute if score @s apRigT matches 7 run function rlk:mboss/apep/rig_stub/stance/crouch
execute if score @s apRigT matches 12 run function rlk:mboss/apep/rig_stub/state/burrowed
execute if score @s apRigT matches 20.. run scoreboard players set @s apRigT 19
