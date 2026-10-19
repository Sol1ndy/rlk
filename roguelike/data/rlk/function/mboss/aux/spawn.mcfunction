# Helper object the player can hit (stars, cores ...), at the execution position. Options set before the
# call: #auxHpPct mb = HP pool in % of the body's max HP (scales with the boss level; preferred), else
# #auxHp mb = fixed HP pool; #auxRes mb = RES %. Invisible NoAI husk with the boss tag (no stun, freeze,
# knockback), rlk_mob + overhead HP bar, a click shield, the boss level; never rlk_zmob. Player hits on it
# take the same modifiers as hits on the body (combat/apply_mods). The new one carries rlk_mb_auxlast until
# the next aux/spawn: add the module's own tags/visuals to it.
tag @e[tag=rlk_mb_auxlast] remove rlk_mb_auxlast
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_hit","boss","rlk_mb_auxlast"],PersistenceRequired:1b,NoAI:1b,NoGravity:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_mb_auxlast,limit=1] at @s run function rlk:mboss/aux/setup
scoreboard players set #auxHp mb 100
scoreboard players set #auxHpPct mb 0
scoreboard players set #auxRes mb 0
scoreboard players set #auxResEl mb -1
scoreboard players set #auxResElV mb 0
