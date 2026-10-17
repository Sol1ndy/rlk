# @s = body, fail clock F = 1..: stars flash 7 and collapse, streams stop 12, sigil breaks 15 + absorption,
# red ring 18, chest starburst 19, smoke + haze off 21, chaos_land 33, chaos_raise 74 (2 spears).
scoreboard players add #gdF mb 1
execute if score #gdF mb matches 1..11 run function rlk:mboss/guardian/chaos/cs_all
execute if score #gdF mb matches 7 run function rlk:mboss/guardian/star/flash
execute if score #gdF mb matches 9 run function rlk:mboss/guardian/star/shrink
execute if score #gdF mb matches 10..14 run execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] at @s run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~1.2 ~ 0.25 0.25 0.25 0 2 force @a[tag=player]
execute if score #gdF mb matches 12 run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs]
execute if score #gdF mb matches 15 run function rlk:mboss/guardian/chaos/sigil_break
execute if score #gdF mb matches 15 run function rlk:mboss/guardian/star/absorb
execute if score #gdF mb matches 15 run playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.8 1.6 0.3
execute if score #gdF mb matches 15 run playsound minecraft:entity.evoker.cast_spell hostile @a[tag=player] ~ ~ ~ 0.6 1 0.3
execute if score #gdF mb matches 16 run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.3 0.5 0.3
execute if score #gdF mb matches 18 run function rlk:mboss/guardian/fx/red_ring
execute if score #gdF mb matches 19 run function rlk:fx/nv/card {kind:"burst",pos:"~ ~6.2 ~",rot:"~ ~",bb:"center",roll:0,spin:30,s0:0.6,s1:4,move:"0f,0f,0f",life:6,fade:3}
execute if score #gdF mb matches 21 run particle minecraft:large_smoke ~ ~5.5 ~ 1.6 0.8 1.6 0.02 30 force @a[tag=player]
execute if score #gdF mb matches 21 run scoreboard players set #gdHaze mb 0
execute if score #gdF mb matches 33 run function rlk:mboss/guardian/rig/play/chaos_land
execute if score #gdF mb matches 55 run playsound minecraft:block.amethyst_block.fall hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.3
execute if score #gdF mb matches 74 if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/rig/play/chaos_raise
execute if score #gdF mb matches 55.. if score #gdFailDone mb matches 1 run return run function rlk:mboss/guardian/chaos/fail_end
execute if score #gdF mb matches 170.. run function rlk:mboss/guardian/chaos/fail_end
