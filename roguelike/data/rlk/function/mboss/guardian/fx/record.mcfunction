# @s = body: record complete, a starburst in the element colour on her (patterns.md §8.2).
execute if score #gdRecEl mb matches 1 run particle minecraft:dust{color:[1f,0.541f,0.298f],scale:1.6} ~ ~2.2 ~ 0.5 0.5 0.5 0 30 force @a[tag=player]
execute if score #gdRecEl mb matches 2 run particle minecraft:dust{color:[0.361f,0.784f,1f],scale:1.6} ~ ~2.2 ~ 0.5 0.5 0.5 0 30 force @a[tag=player]
execute if score #gdRecEl mb matches 3 run particle minecraft:dust{color:[0.894f,0.518f,0.988f],scale:1.6} ~ ~2.2 ~ 0.5 0.5 0.5 0 30 force @a[tag=player]
execute if score #gdRecEl mb matches 4 run particle minecraft:dust{color:[0.635f,0.996f,0.992f],scale:1.6} ~ ~2.2 ~ 0.5 0.5 0.5 0 30 force @a[tag=player]
function rlk:fx/nv/card {kind:"burst",pos:"~ ~2.2 ~",rot:"~ ~",bb:"center",roll:0,spin:30,s0:0.5,s1:2.4,move:"0f,0f,0f",life:5,fade:2}
playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.35 1.5 0.3
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.3
