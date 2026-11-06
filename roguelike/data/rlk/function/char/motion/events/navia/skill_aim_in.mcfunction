function rlk:char/motion/audio/navia/skill_aim_in
# Skill hold, aim-in (owner: skill), started by char/navia/aim_start. Locked for the whole aim (999: never
# unlocks by itself; the next clip releases it). Still holding at the last tick -> the aim loop.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 999
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 16 if score @s nvA matches 1.. run function rlk:char/navia/aim_loop
