function rlk:char/motion/audio/navia/skill_fire
# Skill hold release (owner: skill), started by char/navia/aim_release (charge spent). Locked until the blast.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 3
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 3 if score @s nvShot matches 1.. at @e[tag=rlk_body,limit=1] rotated as @s run function rlk:char/navia/fire
