execute unless entity @e[tag=rlk_mb_body,limit=1] run return run kill @s
scoreboard players operation #pjN mb = @s mbPjV
scoreboard players operation #pjN mb *= #c4 mb
scoreboard players add #pjN mb 9
scoreboard players operation #pjN mb /= #c10 mb
execute if score #pjN mb matches ..0 run scoreboard players set #pjN mb 1
function rlk:mboss/pj/back_step
