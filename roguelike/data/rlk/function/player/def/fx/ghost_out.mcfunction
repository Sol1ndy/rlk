# @s = 붉은 잔상 마네킹(fx/tick: 남은 1틱 · fx/pd_ghost: 새 잔상이 생김). 살아 있는 엔티티라 kill 은 사망 동작과 연기를 보여 준다:
# 테두리(빛남)를 끄고 지도 방이 있는 먼 고정 청크(load 의 forceload 1000000 1000000, 높이 400: 지도 방 y 297~303 의 훨씬 위)로 옮긴다.
# 클라이언트는 추적 범위를 벗어난 엔티티를 그 틱에 바로 지운다(사망 동작 없음). 다음 fx/tick 이 거기서 지운다(cb 1 → 0 → kill)
tag @s remove rlk_cb_ghost
data merge entity @s {Glowing:0b}
execute in minecraft:overworld run tp @s 1000000.5 400 1000000.5
scoreboard players set @s cb 1
