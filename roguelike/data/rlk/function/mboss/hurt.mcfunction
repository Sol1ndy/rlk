# Generic hit on the player. @s = the attacker (hazard marker, projectile, the body for a direct swing);
# it is the knockback source. Inputs: #mbHitPct mb (coefficient %, 100 = registry atk), #cmEl tmp
# (element), #mbKB mb (knockback steps, 0 none), #mbKBDir mb (0 away from @s, 1 along @s's yaw).
# Goes through cm/hit_pl2 -> player/take_damage: dash i-frames, defence, level scaling, element, shields.
# Output: #dodged tmp 1 when the dash i-frames ate the hit.
scoreboard players set #dodged tmp 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
scoreboard players operation #cmDmg tmp = #mbAtk mb
scoreboard players operation #cmDmg tmp *= #mbHitPct mb
scoreboard players operation #cmDmg tmp *= #mbDmgMul mb
scoreboard players operation #cmDmg tmp /= #c10000 mb
execute if score #cmDmg tmp matches ..0 run scoreboard players set #cmDmg tmp 1
scoreboard players operation #cmLv tmp = #mbLv mb
scoreboard players operation #cmKB tmp = #mbKB mb
kill @e[tag=rlk_plkb_source]
execute if score #cmKB tmp matches 1.. run function rlk:mboss/kb_src
execute as @a[tag=player,limit=1] run function rlk:cm/hit_pl2
kill @e[tag=rlk_plkb_source]
scoreboard players set #mbKBDir mb 0
