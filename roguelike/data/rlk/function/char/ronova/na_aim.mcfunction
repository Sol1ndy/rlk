# @s = 플레이어. 1인칭·숄더뷰·F5 모두 플레이어의 실제 눈을 지나는 조준선을 사용한다.
# 시점 함수의 4칸 건너뛰기를 쓰지 않아 가까운 적·벽도 선택한다. 최대 36칸, 0.25칸 간격.
kill @e[tag=rlk_rn_aim]
scoreboard players set #rnAimStep tmp 0
scoreboard players set #rnAimTg tmp 0
execute at @s anchored eyes positioned ^ ^ ^ anchored feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rn_aim"]}
execute at @s anchored eyes positioned ^ ^ ^ anchored feet run function rlk:char/ronova/na_aim_step
