# @s = a collapsing anchor, at it (tick 30, or /reload during the collapse): the implosion, the reward boxes
# (mboss/box/drop_all with #mbPk = riftPk, as the anchor at the spot), then every entity of this rift goes. The zone
# keeps rlk_riftdone.
particle minecraft:reverse_portal ~ ~1.45 ~ 0.3 0.5 0.3 0.6 60
particle minecraft:flash{color:[0.875f,0.965f,1f,1f]} ~ ~1.45 ~ 0 0 0 0 1
scoreboard players operation #mbPk mb = @s riftPk
execute if score #mbPk mb matches 1.. run function rlk:mboss/box/drop_all
scoreboard players operation #riftZid room = @s zid
execute as @e[tag=rlk_rift_part] if score @s zid = #riftZid room run kill @s
kill @s
