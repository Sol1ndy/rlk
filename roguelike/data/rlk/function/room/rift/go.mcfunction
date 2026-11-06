# From mboss/sp/g/<id> (@s = the anchor, at it): the fight starts. The hover object goes, the rift flares (state 3,
# entering), the player is pulled onto the anchor (the spot is a checked 3 x 3 floor with 3 b of headroom) with
# blindness at 20 t; mboss/start_go moves the player into the arena at #spawnT 30.
scoreboard players set @s riftS 3
scoreboard players set @s riftT 0
scoreboard players set @s riftDw 0
scoreboard players operation #riftZid room = @s zid
execute as @e[tag=rlk_rift_obj] if score @s zid = #riftZid room run kill @s
function rlk:room/rift/look/pulse
tp @a[tag=player,limit=1] ~ ~ ~
tp @e[tag=rlk_safe,limit=1] ~ ~ ~
execute as @a[tag=player,limit=1] run function rlk:view/sync
playsound minecraft:block.portal.trigger block @a[tag=player] ~ ~ ~ 0.5 1 0.17
playsound minecraft:entity.enderman.teleport block @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
particle minecraft:reverse_portal ~ ~1.45 ~ 0.8 1.0 0.8 0.05 40
