# 구역 정리 (@s = 구역 표식, at @s): 문 열기. 보스 구역이면 다음 챕터 오브젝트
scoreboard players set @s zst 3
scoreboard players set #combat room 0
execute as @e[tag=rlk_door] run function rlk:room/door_draw
execute as @e[tag=rlk_seal] run function rlk:room/seal_out
execute unless score #k1 snd matches 1 run function rlk:snd/f1
execute unless score #k2 snd matches 1 run function rlk:snd/f2
execute as @a[tag=player,limit=1] run function rlk:room/msg {t:"구역 정리",c:"#8FD46A"}
execute if score @s zkind matches 9 run function rlk:room/obj/k_chapter
