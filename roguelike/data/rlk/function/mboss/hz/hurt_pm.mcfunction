# @s = a per-mille hazard (cm.md 13.11) that reached the player; hz/hurt has marked it hit (and re-armed it). The hit is a
# mboss/pl_dot of mbHzPm per mille of the player's max HP (the hazard's element for the shields, lethal per mbHzPmL; no
# defence, no level factor, no player-side reaction, no knockback) instead of mboss/hurt. Without #hzNoDodge the dash
# i-frames dodge it (#dodged 1, a dodge event; consumed as any hazard hit). Hit / dodge events and the volley group as
# mboss/hurt (source 1); refused while dead, reviving, selecting or with the boss dying (as mboss/hurt).
scoreboard players set #dodged tmp 0
scoreboard players set #mbSrcIn mb 1
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if score #mbSt mb matches 2 run return 0
execute if score @s mbHzND matches 0 as @a[tag=player,scores={dashInvT=1..},limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/dash_iframe
execute if score #dodged tmp matches 1 run return run function rlk:mboss/hurt_dodge
scoreboard players set #mbShIn mb 0
execute if entity @a[tag=player,scores={shieldHP=1..},limit=1] run scoreboard players set #mbShIn mb 1
execute if entity @a[tag=player,scores={gShield=1..},limit=1] run scoreboard players set #mbShIn mb 1
scoreboard players operation #mbDotPct mb = @s mbHzPm
scoreboard players operation #mbDotEl mb = @s mbHzE
scoreboard players operation #mbDotLethal mb = @s mbHzPmL
function rlk:mboss/pl_dot
scoreboard players operation #cmEl tmp = @s mbHzE
function rlk:mboss/hurt_ev
scoreboard players operation #g mb = @s mbHzG
execute if score #g mb matches 1.. run function rlk:mboss/grp_mark
