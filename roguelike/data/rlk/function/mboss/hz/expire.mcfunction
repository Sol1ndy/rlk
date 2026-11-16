execute if score @s mbHzV matches 1.. run scoreboard players set #hzEv mb 2
execute if score @s mbHzV matches 1.. run function rlk:mboss/d/hz_vis
# a mask with its own safe group (#hzSafeG 0 at creation) takes its safe markers with it (AZ-CM)
execute if score @s mbHzK matches 6 if score @s mbHzSG = @s mbHzI run function rlk:mboss/hz/mask_end
kill @s
