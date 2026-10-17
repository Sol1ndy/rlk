# The common hitbox body (call from the module's spawn hook, at the spawn point; context yaw = facing).
# Invisible NoAI husk: rlk_zmob holds the zone fight, boss gives stun/freeze/knockback immunity,
# miniboss switches the boss economy to #mbGoldMul / #mbSap. HP/XP/level come from rlk:mboss cur.
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_mboss","boss","miniboss","rlk_mb_body","rlk_mb_inv","rlk_mb_bnew"],PersistenceRequired:1b,NoAI:1b,NoGravity:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_mb_bnew,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_mb_bnew,limit=1] at @s run function rlk:mboss/body_setup
tag @e[tag=rlk_mb_bnew] remove rlk_mb_bnew
