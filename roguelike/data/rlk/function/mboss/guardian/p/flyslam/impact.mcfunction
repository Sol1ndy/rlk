# @s = body on the ring centre (clip tick 41): the hazard strikes this tick (framework).
tag @s remove rlk_mb_inv
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5r] run data merge entity @s {block_state:{id:"minecraft:white_stained_glass"}}
function rlk:fx/nv/card {kind:"burst",pos:"~ ~1.3 ~",rot:"~ ~",bb:"center",roll:0,spin:20,s0:0.8,s1:4.6,move:"0f,0f,0f",life:6,fade:3}
function rlk:fx/nv/card {kind:"glow",pos:"~ ~1.6 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:2,s1:7,move:"0f,0f,0f",life:5,fade:2}
function rlk:fx/nv/card {kind:"ring",pos:"~ ~0.12 ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1,s1:10.5,move:"0f,0f,0f",life:8,fade:3}
particle minecraft:dust{color:[1f,1f,0.99f],scale:2.4} ~ ~1 ~ 0.8 0.8 0.8 0 30 force @a[tag=player]
particle minecraft:dust{color:[0.992f,0.961f,0.706f],scale:1.8} ~ ~0.4 ~ 2 0.2 2 0 40 force @a[tag=player]
particle minecraft:explosion ~ ~0.6 ~ 1.2 0.2 1.2 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.4 ~ 2.2 0.3 2.2 0.2 40 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:brown_terracotta"} ~ ~0.4 ~ 1.6 0.3 1.6 0.25 24 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.9 0.33
playsound minecraft:entity.zombie.attack_iron_door hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.23
