# 0.1초 경직 (@s = 몹). 슬로우로 이동만 막고 넉백 물리는 유지 보스는 경직을 받지 않는다
execute if entity @s[tag=boss] run return 0
execute if entity @s[tag=rlk_cm_cn] run return 0
# 커스텀 몹 차지 중: 경직 면역
execute if entity @s[tag=rlk_cmch] run return 0
effect give @s minecraft:slowness 1 250 true
scoreboard players set @s stunT 2
# 어그로 풀기: 몸과 같은 팀으로
team join rlk_stun @s
