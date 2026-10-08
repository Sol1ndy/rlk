# @s = 예약 표식, at @s. 씨앗이 붙은 모든 적(20칸)에게 공격력의 40퍼센트 풀 원소 피해
execute store result score #now itv run time query gametime
execute as @e[tag=rlk_mob,distance=..20] if score @s skEnd > #now itv run tag @s add rlk_skt
execute at @e[tag=rlk_skt] run particle minecraft:happy_villager ~ ~1.2 ~ 0.3 0.5 0.3 0 12
execute if entity @e[tag=rlk_skt,limit=1] run playsound minecraft:block.azalea_leaves.break master @a ~ ~ ~ 0.8 1.3
execute as @a[tag=player,limit=1] run function rlk:items/proc/skandha_calc
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 7
scoreboard players set #elU tmp 1000
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_skt] add rlk_hit
tag @e[tag=rlk_skt] remove rlk_skt
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #sub itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
