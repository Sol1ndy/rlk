function rlk:char/motion/audio/navia/skill
# Skill tap (owner: skill), started by char/navia/tap (the charge is already spent). Locked until the shot;
# the shot itself (pellets, damage, Geo passive, muzzle fx and blast sound, first-person gun) is char/navia/fire.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 7
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 7 if score @s nvShot matches 1.. at @e[tag=rlk_body,limit=1] rotated as @s run function rlk:char/navia/fire
