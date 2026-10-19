# Generic hit on the player. @s = the attacker (hazard marker, projectile, the body for a direct swing);
# it is the knockback source. Inputs: #mbHitPct mb (coefficient %, 100 = registry atk), #cmEl tmp
# (element), #mbKB mb (knockback steps, 0 none), #mbKBDir mb (0 away from @s, 1 along @s's yaw).
# Goes through cm/hit_pl2 -> player/take_damage: dash i-frames, defence, level scaling, element, shields.
# Output: #dodged tmp 1 when the dash i-frames ate the hit. #mbNoDodge mb 1 (set around the call by hz/hurt for a
# #hzNoDodge hazard): the dash i-frames are ignored for this one hit (the player keeps them for the next).
# Chapter mode (AZ-CM, cm.md 13.3 / 13.4): one-shot inputs #mbNoRx (no player-side reaction: F:player/take_damage skips
# element/player_hit while #mbNRNow 1; hz/hurt and pj/hit copy their hazard's / prop's option into it) and #mbSrc
# (1 hazard, 2 projectile; 0 = a direct call); refused while #mbCine 1; after a call that reached the player the hit /
# dodge events #mbHitEv #mbHitEl #mbHitSh #mbHitRA #mbHitSrc / #mbDodgeEv #mbDodgeOk (read and cleared by the module).
scoreboard players set #dodged tmp 0
scoreboard players operation #mbNRIn mb = #mbNoRx mb
scoreboard players set #mbNoRx mb 0
scoreboard players operation #mbSrcIn mb = #mbSrc mb
scoreboard players set #mbSrc mb 0
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
execute if score #mbCine mb matches 1 run return 0
scoreboard players set #mbShIn mb 0
execute if entity @a[tag=player,scores={shieldHP=1..},limit=1] run scoreboard players set #mbShIn mb 1
execute if entity @a[tag=player,scores={gShield=1..},limit=1] run scoreboard players set #mbShIn mb 1
scoreboard players operation #mbNRNow mb = #mbNRIn mb
scoreboard players operation #cmDmg tmp = #mbAtk mb
scoreboard players operation #cmDmg tmp *= #mbHitPct mb
scoreboard players operation #cmDmg tmp *= #mbDmgMul mb
scoreboard players operation #cmDmg tmp /= #c10000 mb
execute if score #cmDmg tmp matches ..0 run scoreboard players set #cmDmg tmp 1
scoreboard players operation #cmLv tmp = #mbLv mb
scoreboard players operation #cmKB tmp = #mbKB mb
kill @e[tag=rlk_plkb_source]
execute if score #cmKB tmp matches 1.. run function rlk:mboss/kb_src
execute unless score #mbNoDodge mb matches 1 as @a[tag=player,limit=1] run function rlk:cm/hit_pl2
# #mbNoDodge mb 1 (a #hzNoDodge hazard): dash i-frames do not help this hit
execute if score #mbNoDodge mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/hurt_nd
scoreboard players set #mbNRNow mb 0
kill @e[tag=rlk_plkb_source]
scoreboard players set #mbKBDir mb 0
function rlk:mboss/hurt_ev
