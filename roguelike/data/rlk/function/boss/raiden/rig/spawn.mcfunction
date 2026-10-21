# @s = the boss (the anchor), at its feet. Summons the 30 parts (fixed UUIDs) in the rest pose of the stored state
# (rdRigS: 1 = Tenma, else Shogun), re-applies the looks and queues the state's idle clip.
function rlk:boss/raiden/rig/init
function rlk:boss/raiden/rig/kill
execute unless score @s rdRigS matches 0..2 run scoreboard players set @s rdRigS 0
execute unless score @s rdRigW matches 0..1 run scoreboard players set @s rdRigW 0
execute if score @s rdRigS matches 2 run scoreboard players set @s rdRigS 0
execute if score @s rdRigS matches 1 run function rlk:boss/raiden/rig/spawn_tenma
execute unless score @s rdRigS matches 1 run function rlk:boss/raiden/rig/spawn_shogun
scoreboard players set @s rdRigF 0
execute rotated as @s rotated ~ 0 run function rlk:boss/raiden/rig/follow_now
