# @s = a per-mille hazard (cm.md 13.11) that reached the player; hz/hurt has marked it hit (and re-armed it). The hit is a
# mboss/pl_dot of mbHzPm per mille of the player's max HP (the hazard's element for the shields, lethal per mbHzPmL; no
# defence, no level factor, no player-side reaction, no knockback) instead of mboss/hurt. Without #hzNoDodge the i-frames
# or a perfect dodge avoid it (player/def/judge: #dodged 1, a dodge event; consumed as any hazard hit; unparriable by the
# default rule hz/np_def, so a tier-1/2 parry takes the full hit). Hit / dodge events and the volley group as
# mboss/hurt (source 1); refused while dead, reviving, selecting or with the boss dying (as mboss/hurt).
scoreboard players set #dodged tmp 0
scoreboard players set #mbSrcIn mb 1
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
# combat overhaul C: the parry / dodge judge with this hit's context (boss, area, unparriable mbHzNP, no-dodge mbHzND); a
# parry never reduces a per-mille hit (only an avoided hit counts: #dodged 1)
function rlk:mboss/hurt_ctx
scoreboard players set #hcK tmp 3
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/def/judge
execute if score #dodged tmp matches 1 run return run function rlk:mboss/hurt_dodge
scoreboard players set #mbShIn mb 0
execute if entity @a[tag=player,scores={shieldHP=1..},limit=1] run scoreboard players set #mbShIn mb 1
execute if entity @a[tag=player,scores={gShield=1..},limit=1] run scoreboard players set #mbShIn mb 1
# ar FN-1: a Bond-of-Life per-mille hazard (mbBol) goes on in hz/hurt_pm_bol
execute if score @s mbBol matches 1.. run return run function rlk:mboss/hz/hurt_pm_bol
scoreboard players operation #mbDotPct mb = @s mbHzPm
scoreboard players operation #mbDotEl mb = @s mbHzE
scoreboard players operation #mbDotLethal mb = @s mbHzPmL
function rlk:mboss/pl_dot
scoreboard players operation #cmEl tmp = @s mbHzE
function rlk:mboss/hurt_ev
scoreboard players operation #g mb = @s mbHzG
execute if score #g mb matches 1.. run function rlk:mboss/grp_mark
