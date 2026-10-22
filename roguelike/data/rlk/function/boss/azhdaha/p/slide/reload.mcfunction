# /reload inside the landslide: the hazards are gone, the clock goes on and the next wave comes (plan 4.3). A cut
# walk ends at the centre at once. (The rig respawns in idle: it cannot resume a clip mid-way, so the remaining
# waves keep their sounds but not the lift poses.)
scoreboard players set #mbNoLeash mb 1
execute if score #azPT mb matches ..39 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run tp @s ~ ~ ~
execute if score #azPT mb matches ..39 run scoreboard players set #aq20M mb 0
