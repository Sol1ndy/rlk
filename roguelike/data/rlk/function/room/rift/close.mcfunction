# From mboss/sp/reward (@s = the anchor, at it; #spPk mb = the boxes): the collapse (30 t: the rim shrinks, the arcs
# snap inward, an implosion), then room/rift/close_end drops the boxes on the spot and removes the rift.
scoreboard players set @s riftS 4
scoreboard players set @s riftT 0
scoreboard players operation @s riftPk = #spPk mb
scoreboard players operation #riftZid room = @s zid
execute as @e[tag=rlk_rift_obj] if score @s zid = #riftZid room run kill @s
function rlk:room/rift/look/close
playsound minecraft:block.respawn_anchor.deplete block @a[tag=player] ~ ~ ~ 0.8 1 0.27
playsound minecraft:block.beacon.deactivate block @a[tag=player] ~ ~ ~ 0.6 1 0.2
