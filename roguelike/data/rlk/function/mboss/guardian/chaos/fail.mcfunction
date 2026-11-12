# @s = body, fail clock F = 1.. (the m4 schedule x0.75): stars flash 5 and collapse, streams stop 9, sigil
# breaks 11 + absorption, red ring 14, chest starburst 14, smoke + haze off 16, chaos_land 25,
# chaos_raise 54 (2 spears).
scoreboard players add #gdF mb 1
execute if score #gdF mb matches 1..8 run function rlk:mboss/guardian/chaos/cs_all
execute if score #gdF mb matches 5 run function rlk:mboss/guardian/star/flash
execute if score #gdF mb matches 7 run function rlk:mboss/guardian/star/shrink
execute if score #gdF mb matches 8..10 run execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_starv] at @s run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~1.2 ~ 0.25 0.25 0.25 0 2 force @a[tag=player]
execute if score #gdF mb matches 9 run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs]
execute if score #gdF mb matches 11 run function rlk:mboss/guardian/chaos/sigil_break
execute if score #gdF mb matches 11 run function rlk:mboss/guardian/star/absorb
execute if score #gdF mb matches 11 run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.8 1.6 0.27
execute if score #gdF mb matches 11 run playsound minecraft:entity.evoker.cast_spell hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
execute if score #gdF mb matches 12 run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.3 0.5 0.1
execute if score #gdF mb matches 14 run function rlk:mboss/guardian/fx/red_ring
execute if score #gdF mb matches 15 run function rlk:fx/nv/card {kind:"burst",pos:"~ ~6.2 ~",rot:"~ ~",bb:"center",roll:0,spin:30,s0:0.6,s1:4,move:"0f,0f,0f",life:6,fade:3}
execute if score #gdF mb matches 16 run particle minecraft:large_smoke ~ ~5.5 ~ 1.6 0.8 1.6 0.02 30 force @a[tag=player]
execute if score #gdF mb matches 16 run scoreboard players set #gdHaze mb 0
execute if score #gdF mb matches 25 run function rlk:mboss/guardian/rig/play/chaos_land
execute if score #gdF mb matches 47 run playsound minecraft:block.amethyst_block.fall hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.27
execute if score #gdF mb matches 54 if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/rig/play/chaos_raise
execute if score #gdF mb matches 47.. if score #gdFailDone mb matches 1 run return run function rlk:mboss/guardian/chaos/fail_end
execute if score #gdF mb matches 47.. if score #gdPRel mb matches 1 run return run function rlk:mboss/guardian/chaos/fail_end
execute if score #gdF mb matches 170.. run function rlk:mboss/guardian/chaos/fail_end
