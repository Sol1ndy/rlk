# 구역 정리 (@s = 구역 표식, at @s): 문 열기. 보스 구역이면 다음 챕터 오브젝트
scoreboard players set @s zst 3
scoreboard players set #combat room 0
execute as @e[tag=rlk_door] run function rlk:room/door_draw
execute as @e[tag=rlk_seal] run function rlk:room/seal_out
execute unless score #k1 snd matches 1 run function rlk:snd/f1
execute unless score #k2 snd matches 1 run function rlk:snd/f2
execute as @a[tag=player,limit=1] run function rlk:room/msg {t:"구역 정리",c:"#8FD46A"}
# rift (build_rift.py)
execute if entity @s[tag=rlk_riftz] if score #spOn mb matches 1 run return run function rlk:mboss/sp/clear
# rift (build_rift.py)
execute if entity @s[tag=rlk_riftz] run function rlk:room/rift/open
# 챕터 보스 구역: 경기장 정리 → 귀환 → 처치했으면 다음 챕터 오브젝트, 취소면 문이 다시 나타남(mboss/cb/clear)
execute if score @s zkind matches 9 if data entity @s data.cboss run return run function rlk:mboss/cb/clear
execute if score @s zkind matches 9 unless score #rdTest rd matches 1 run function rlk:room/obj/k_chapter
# 보스 테스트(boss/raiden/test/start) 중이면 다음 챕터 대신 다시 하기 / 로비로 안내
execute if score @s zkind matches 9 if score #rdTest rd matches 1 run function rlk:boss/raiden/test/won
# 중간보스 구역: 경기장 정리 → 던전으로 귀환 → 처치했으면 아이템 선택 2번(취소면 보상 없이 문이 다시 나타남)
execute if score @s zkind matches 15 run function rlk:mboss/won
