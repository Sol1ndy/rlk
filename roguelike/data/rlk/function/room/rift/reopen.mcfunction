# From mboss/sp/won_cancel (@s = the anchor, at it): the fight was cancelled, the rift is open again; the returning
# player (1.2 - 2 b in front of it) gets 60 t before a walk-in counts.
function rlk:room/rift/open_now
scoreboard players set @s riftCd 60
playsound minecraft:block.end_portal.spawn block @a[tag=player] ~ ~ ~ 0.4 1.5 0.13
