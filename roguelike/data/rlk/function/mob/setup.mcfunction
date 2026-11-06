# 새 몹 (@s = 몹, at @s)
# 액자 등 생명체가 아닌 엔티티에는 전투 태그와 체력바를 만들지 않는다.
execute unless data entity @s Health run return 0
attribute @s minecraft:knockback_resistance base set 0.5
execute if entity @s[tag=rlk_raiden] run attribute @s minecraft:knockback_resistance base set 1
execute if entity @s[tag=rlk_raiden] run attribute @s minecraft:explosion_knockback_resistance base set 1
execute if entity @s[tag=rlk_cm_cn] run attribute @s minecraft:knockback_resistance base set 1
execute if entity @s[tag=rlk_mb_body] run attribute @s minecraft:knockback_resistance base set 1
execute if entity @s[tag=rlk_mb_body] run attribute @s minecraft:explosion_knockback_resistance base set 1
execute if entity @s[tag=rlk_cm_cn] run attribute @s minecraft:explosion_knockback_resistance base set 1
# 추적 거리: 아무리 멀어도 놓치지 않게
attribute @s minecraft:follow_range base set 128
# 중간보스 몸체는 머리 위 체력바 대신 보스바(원소 부착 아이콘 포함). 보조 오브젝트(별)는 머리 위 바를 씀
execute unless entity @s[tag=rlk_raiden] unless entity @s[tag=rlk_rd_object] unless entity @s[tag=rlk_mb_body] run function rlk:mob/hb_spawn
# 레벨이 없는 몹은 1레벨
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
# 체력 스코어 준비(이미 정해진 몹은 그대로)
execute unless score @s mhpM matches 1.. run function rlk:mob/hp_init
tag @s add rlk_mob
# 숄더뷰: 아바타를 노리게
execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/mob_join
