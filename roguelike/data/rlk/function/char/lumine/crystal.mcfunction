# 얼음 결정 (@s = 맞는 몹): 별에서 몹까지 궤적을 그리고 공격력의 50% 얼음 원소 피해. 적중 = 차가운 별빛 +1, 두 번에 한 번 원소 입자 1개
tag @s add rlk_ctgt
execute at @e[tag=rlk_lstar,limit=1] facing entity @s eyes run function rlk:char/lumine/crystal_trail
tag @s remove rlk_ctgt
execute at @e[tag=rlk_lstar,limit=1] unless score #k345 snd matches 1 run function rlk:snd/f410
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:50}
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 4
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
execute at @s run function rlk:combat/apply
execute at @s run particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 0.25 0.3 0.25 0.1 10
execute as @a[tag=player,limit=1] run scoreboard players add @s[scores={starlight=..7}] starlight 1
scoreboard players add @e[tag=rlk_lstar,limit=1] pcVal 1
execute if score @e[tag=rlk_lstar,limit=1] pcVal matches 2.. at @s positioned ~ ~1 ~ run function rlk:char/particles {n:1,el:4}
execute if score @e[tag=rlk_lstar,limit=1] pcVal matches 2.. run scoreboard players set @e[tag=rlk_lstar,limit=1] pcVal 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
