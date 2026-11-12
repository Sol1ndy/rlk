# 이번 틱에 플레이어의 퍼펙트 창이 열려 있으면 성공(1): 닷지를 0..#dgPW-1 틱 전에, 또는 F 를 0..#parW3-1 틱 전에 받았다
# (아무 실행자; 홍련의 방패 조각 boss/scarlet/shield/pip 같은 "그 공격을 퍼펙트로 넘겼나" 판정용, 공격이 실제로 닿지 않아도 됨)
execute store result score #qn cb run time query gametime
scoreboard players operation #qn cb -= #btAdj cb
execute as @a[tag=player,limit=1] run return run function rlk:player/def/q_pf
return fail
