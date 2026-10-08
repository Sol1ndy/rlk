# 창공을 울리는 포성 (@s = 플레이어, at 몸): 앞쪽 범위(4칸 앞을 중심으로 반경 5칸 + 발동 자리 반경 2.5칸) 포격 → #nvQDur 틱 동안 #nvQGap 틱마다 지원 포격
function rlk:char/dmg_calc {coef:120}
function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 5
scoreboard players set #elU tmp 1000
tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^4 run tag @e[tag=rlk_mob,distance=..5] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
execute as @e[tag=rlk_hit] at @s run function rlk:char/navia/shell_fx
tag @e[tag=rlk_hit] remove rlk_hit
function rlk:char/after_hit
execute if score #hitLanded tmp matches 1 run function rlk:char/navia/q_shard
execute rotated ~ 0 positioned ^ ^ ^4 run particle minecraft:explosion ~ ~1 ~ 2.0 0.4 2.0 0 6
execute rotated ~ 0 positioned ^ ^ ^4 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.5 ~ 2.5 0.5 2.5 0.2 60
playsound minecraft:entity.generic.explode master @a ~ ~ ~ 1.0 0.8
playsound minecraft:entity.firework_rocket.large_blast master @a ~ ~ ~ 1.0 0.7
scoreboard players operation @s nvQ = #nvQDur tmp
scoreboard players set @s nvQT 0
