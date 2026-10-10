# 전투 시작 (@s = 구역 표식, at @s): 이 구역의 문을 잠그고 잠시 뒤 적 소환
scoreboard players operation #combat room = @s zid
scoreboard players set #spawnT room 20
execute as @e[tag=rlk_door] run function rlk:room/door_draw
# 안 가 본 쪽 통로(검은 콘크리트)에는 붉은 봉인 무늬: 적이 남아 있어 지나갈 수 없음
execute as @e[tag=rlk_door,scores={dst=1}] run function rlk:room/seal_check
execute unless score #k5 snd matches 1 run function rlk:snd/f5
execute as @a[tag=player,limit=1] run function rlk:room/msg {t:"적 출현",c:"#E06A5A"}
