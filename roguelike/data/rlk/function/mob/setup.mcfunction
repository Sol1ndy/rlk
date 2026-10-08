# 새 몹 (@s = 몹, at @s)
attribute @s minecraft:knockback_resistance base set 0.5
# 추적 거리: 아무리 멀어도 놓치지 않게
attribute @s minecraft:follow_range base set 128
function rlk:mob/hb_spawn
# 레벨이 없는 몹은 1레벨
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
# 체력 스코어 준비(이미 정해진 몹은 그대로)
execute unless score @s mhpM matches 1.. run function rlk:mob/hp_init
tag @s add rlk_mob
# 숄더뷰: 아바타를 노리게
execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/mob_join
