# 느린 화면의 세계 틱(5 · 8 · 11틱) 뒤: 이 틱에 자세를 받은 세계 쪽 디스플레이 — 보스 리그(rlk_mb_part) · 보스 투사체(rlk_mb_pj) ·
# 나루카미 리그(rlk_raiden_part) · 커스텀 몹의 리그(rlk_cmlink)와 투사체(rlk_cmp) — 의
# interpolation_duration 을 3배로(다음 세계 틱이 3틱 뒤이므로). 한 번 늘인 값은 점수 btD 에 적어 두고, 값이 그대로면(그 뒤 자세를 받지
# 않음) 다시 건드리지 않는다. 플레이어 쪽(아바타 리그 · 효과)은 제 속도라 늘이지 않는다.
# 디스플레이의 NBT 를 쓰면 클라이언트가 보간을 처음부터 다시 돌리므로(Display.readAdditionalSaveData 가 start_interpolation 을 늘 강제로
# 보냄) 같은 쓰기에 그림자 세기를 조금 바꿔 넣는다: 그러면 "지금 보이는 자세에서 목표까지 새 길이로" 가 된다(review/v/client_facts.md,
# vp_progress.md). 그림자가 있는 디스플레이(shadow_radius 0 아님)는 건드리지 않는다
scoreboard players add #btStN cb 1
scoreboard players set #btSt cb 1
data modify storage rlk:bt n set value "0.99"
execute if score #btStN cb matches 2 run data modify storage rlk:bt n set value "0.98"
execute if score #btStN cb matches 2 run scoreboard players set #btStN cb 0
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_mb_part,distance=..48] run function rlk:player/def/beat/st/one
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_mb_pj,distance=..48] run function rlk:player/def/beat/st/one
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_raiden_part,distance=..48] run function rlk:player/def/beat/st/one
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_cmlink,distance=..48] run function rlk:player/def/beat/st/one
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_cmp,distance=..48] run function rlk:player/def/beat/st/one
