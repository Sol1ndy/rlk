function rlk:char/motion/audio/navia/skill_aim
# Skill hold, aim loop (owner: skill; loop:true). Lock re-armed on every wrap. Released by char/navia/aim_tick
# -> aim_release (starts skill_fire). Self-heal: an aim that ended without a release clip finishes the loop.
execute unless score @s nvA matches 1.. run return run function rlk:char/motion/finish
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 999
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
