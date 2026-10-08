# @s = 예약 표식, at @s. 반경 3칸에 공격력의 40퍼센트 바위 원소 피해
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.3f} ~ ~0.6 ~ 1.2 0.4 1.2 0 30
particle minecraft:block{block_state:"minecraft:yellow_terracotta"} ~ ~0.4 ~ 1.0 0.2 1.0 0.1 20
playsound minecraft:block.amethyst_block.break master @a ~ ~ ~ 0.6 0.9
scoreboard players set #aqE eng 5
tag @e[tag=rlk_mob,distance=..3,sort=nearest,limit=1] add rlk_abt
execute if entity @e[tag=rlk_abt,limit=1] at @e[tag=rlk_blossom,limit=1,sort=nearest] positioned ~ ~0.4 ~ facing entity @e[tag=rlk_abt,limit=1] eyes run function rlk:items/fx/shot
tag @e[tag=rlk_abt] remove rlk_abt
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:60}
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 5
scoreboard players set #elU tmp 1000
scoreboard players set #blossomHit itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..3] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #blossomHit itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
kill @s
scoreboard players set #sub itv 0
