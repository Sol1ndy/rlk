# Core service 61 (phase 3): toggle the stance (UPRIGHT -> crouch_p3, CROUCH -> stand_p3).
scoreboard players set #apX mb 0
execute if score #apStance mb matches 1 run scoreboard players set #apX mb 1
execute if score #apX mb matches 1 run function rlk:mboss/apep/play/crouch_p3
execute if score #apX mb matches 0 run function rlk:mboss/apep/play/stand_p3
scoreboard players operation #apMvK mb = #apX mb
