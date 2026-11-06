# finish (ON_FINISH), phase 0, as the boss: back to the weapon idle; queue a rear check when the player
# hit her from behind within 40 t and stands behind her now (she keeps her facing for it).
function rlk:boss/raiden/sg/idle_clip
scoreboard players set @s rdSgV 0
scoreboard players set @s rdSgGs 0
scoreboard players set @s rdSgCt 0
scoreboard players set @s rdSgRearQ 0
scoreboard players set #rdSgRear rd 0
execute if score @s rdSgRearT matches 1.. if score @s rdSgRearCD matches ..0 at @s run function rlk:boss/raiden/sg/rear_test
execute if score #rdSgRear rd matches 1 run scoreboard players set @s rdSgRearQ 1
execute if score @s rdSgRearQ matches 1 run scoreboard players set @s rdCool 4
