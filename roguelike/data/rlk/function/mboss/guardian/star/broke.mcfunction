# @s = a broken star husk (rlk_mb_broken from aux/take). 1st break -> 6 %, 2nd -> 18 % + groggy, each
# 5 t later (patterns.md §9.3). Number colour = the star colour.
scoreboard players add #gdBrk mb 1
scoreboard players remove #gdStars mb 1
scoreboard players operation #gdX mb = @s mbS
execute if score #gdX mb matches 5 run scoreboard players set #gdX mb 5
execute if score #gdX mb matches 6 run scoreboard players set #gdX mb 2
execute if score #gdBrk mb matches 1 run scoreboard players set #gdBq1 mb 6
execute if score #gdBrk mb matches 1 run scoreboard players operation #gdBe1 mb = #gdX mb
execute if score #gdBrk mb matches 2.. run scoreboard players set #gdBq2 mb 6
execute if score #gdBrk mb matches 2.. run scoreboard players operation #gdBe2 mb = #gdX mb
scoreboard players operation #gdX mb = @s mbId
execute if score #gdX mb matches 1 run scoreboard players set #gdSa1 mb 0
execute if score #gdX mb matches 2 run scoreboard players set #gdSa2 mb 0
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_starv] if score @s mbId = #gdX mb run kill @s
execute if score @s mbS matches 1 run particle minecraft:dust{color:[1f,0.541f,0.298f],scale:1.8} ~ ~1.3 ~ 0.4 0.5 0.4 0 30 force @a[tag=player]
execute if score @s mbS matches 2 run particle minecraft:dust{color:[0.361f,0.784f,1f],scale:1.8} ~ ~1.3 ~ 0.4 0.5 0.4 0 30 force @a[tag=player]
execute if score @s mbS matches 3 run particle minecraft:dust{color:[0.824f,0.51f,0.98f],scale:1.8} ~ ~1.3 ~ 0.4 0.5 0.4 0 30 force @a[tag=player]
execute if score @s mbS matches 4 run particle minecraft:dust{color:[0.635f,0.996f,0.992f],scale:1.8} ~ ~1.3 ~ 0.4 0.5 0.4 0 30 force @a[tag=player]
execute if score @s mbS matches 5 run particle minecraft:dust{color:[0.988f,0.898f,0.51f],scale:1.8} ~ ~1.3 ~ 0.4 0.5 0.4 0 30 force @a[tag=player]
execute if score @s mbS matches 6 run particle minecraft:dust{color:[0.651f,0.808f,0.992f],scale:1.8} ~ ~1.3 ~ 0.4 0.5 0.4 0 30 force @a[tag=player]
particle minecraft:end_rod ~ ~1.3 ~ 0.2 0.3 0.2 0.12 14 force @a[tag=player]
execute if score #gdBrk mb matches 1 run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute if score #gdBrk mb matches 1 run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute if score #gdBrk mb matches 2.. run playsound minecraft:block.amethyst_block.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute if score #gdBrk mb matches 2.. run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 1.4 0.33
execute if score #gdBrk mb matches 2.. run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.3 2 0.1
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/guardian/fx/star_hit
kill @s
execute if score #gdBrk mb matches 2.. as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/guardian/chaos/success
execute if score #gdBrk mb matches 1 run function rlk:mboss/guardian/hud/sub_chaos
