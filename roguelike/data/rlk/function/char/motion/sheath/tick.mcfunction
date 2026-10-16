# @s player, every rig tick after loco/observe and before the clip or locomotion.
execute unless score @s pmSheath matches 0.. run scoreboard players set @s pmSheath 1
# Self-heal: a put-away state without its clip (release without finish) counts as drawn, retry in 1 s.
execute if score @s pmSheath matches 2 unless score @s pmActive matches 1 run scoreboard players set @s pmShT 20
execute if score @s pmSheath matches 2 unless score @s pmActive matches 1 run scoreboard players set @s pmSheath 0
# Moving during the put-away clip: quick stow and blend into sheathed locomotion.
execute if score @s pmActive matches 1 if data storage rlk:player_motion active{clip:"sheathe"} unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort
execute unless score @s pmSheath matches 0 run return 0
execute if score @s pmActive matches 1 run return 0
execute if score @s rdCam matches 1 run return 0
execute if score @s pmShT matches 1.. run scoreboard players remove @s pmShT 1
execute if score @s pmShT matches 1.. run return 0
# Delay over: first person, moving or airborne = quick stow; idle on the ground = put-away clip.
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:char/motion/sheath/stow
execute unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/stow
function rlk:char/motion/sheath/begin
