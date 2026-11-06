tp @s @e[tag=rlk_rv_tsel,limit=1]
function rlk:cm/rv/tgt_kill
tag @s remove rlk_rv_lk
# crashed: 30 t on the ground, stunnable (the punish window)
scoreboard players set @s cmS 4
scoreboard players set @s cmT 30
tag @s remove rlk_cmch
tag @s remove rlk_c2_fix
execute at @s run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.2 ~ 0.8 0.15 0.8 0.1 40
execute at @s run particle minecraft:flame ~ ~0.3 ~ 0.7 0.1 0.7 0.04 14
execute at @s run particle minecraft:large_smoke ~ ~0.4 ~ 0.6 0.2 0.6 0.02 8
execute at @s run playsound minecraft:entity.generic.big_fall master @a ~ ~ ~ 1 0.7
execute at @s run playsound minecraft:block.fire.extinguish master @a ~ ~ ~ 0.7 0.9
