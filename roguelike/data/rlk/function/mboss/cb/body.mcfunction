# The chapter boss's hitbox body (the module's spawn hook calls this instead of mboss/body; at the spawn point, context
# yaw = facing): as mboss/body WITHOUT miniboss (the boss economy: gold x15 x chapter, 2 sapphires, combat/gold_drop),
# rlk_mb_big when cur.px (proxy redirect, px/dup), rlk_mb_noshield when cur.shield is 0b (no click box in any state).
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_mboss","boss","rlk_mb_body","rlk_mb_inv","rlk_mb_bnew"],PersistenceRequired:1b,NoAI:1b,NoGravity:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_mb_bnew,limit=1] run tp @s ~ ~ ~ ~ 0
execute if data storage rlk:mboss cur{px:1b} run tag @e[tag=rlk_mb_bnew] add rlk_mb_big
execute if data storage rlk:mboss cur{shield:0b} run tag @e[tag=rlk_mb_bnew] add rlk_mb_noshield
execute as @e[tag=rlk_mb_bnew,limit=1] at @s run function rlk:mboss/body_setup
tag @e[tag=rlk_mb_bnew] remove rlk_mb_bnew
