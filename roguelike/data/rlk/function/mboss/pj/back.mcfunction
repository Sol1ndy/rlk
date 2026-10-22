# Return leg: steer at the body's eyes (facing entity .. eyes); arrived = the prop touches the body's hitbox
# (a 1-block cube around the prop intersects it; the eye point lies inside the hitbox at any scale). A
# moving body can outrun the prop, so the time cap from pj/turn ends the leg with event 3 anyway.
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run return run kill @s
execute if score @s mbPjT > @s mbPjL run return run function rlk:mboss/pj/returned
scoreboard players operation #pjN mb = @s mbPjV
scoreboard players operation #pjN mb *= #c4 mb
scoreboard players add #pjN mb 9
scoreboard players operation #pjN mb /= #c10 mb
execute if score #pjN mb matches ..0 run scoreboard players set #pjN mb 1
function rlk:mboss/pj/back_step
