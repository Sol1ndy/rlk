# @s = 인형의 표식, at @s. 폭발: 반경 4칸에 공격력의 100퍼센트 불 원소 피해. 숄더뷰면 적의 시선을 다시 아바타로
kill @e[tag=rlk_decoy]
particle minecraft:explosion ~ ~0.8 ~ 0.6 0.4 0.6 0 4
particle minecraft:flame ~ ~0.8 ~ 1.2 0.6 1.2 0.08 60
execute unless score #k64 snd matches 1 run function rlk:snd/f122
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:100}
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players operation #dmgBase tmp = #dmg tmp
tag @e[tag=rlk_mob,distance=..4] add rlk_hit
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute if entity @e[tag=rlk_av,limit=1] as @e[tag=rlk_mob,tag=!rlk_cmb,distance=..14] run damage @s 0 minecraft:generic by @e[tag=rlk_av,limit=1]
kill @s
scoreboard players set #sub itv 0
