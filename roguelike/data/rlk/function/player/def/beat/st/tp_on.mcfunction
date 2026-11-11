# 느린 화면에 들어가는 틱(5틱, 그 틱의 이동 뒤): 틱마다 tp 로 움직이는 세계 쪽 디스플레이의 teleport_duration(1~19)을 3배로. 클라이언트는
# 이동 패킷을 길이보다 먼저 받으므로 한 틱 앞서 바꾼다(다음 이동 = 8틱)
scoreboard players set #btTp cb 1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_mb_part,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_mb_pj,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_raiden_part,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_cmlink,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_cmp,distance=..48] run function rlk:player/def/beat/st/tp1
# 홍련의 검 끝 경로 · 표적 선 · 그 머리(rlk_hr_sw: tools/mboss_scarlet/blade.py; 패턴 틱마다 tp, teleport_duration 1)도 같이 늘인다 — 리그와
# 같은 속도로 미끄러지게(11-12 V 통합: 레인 VB 의 요청). 느린 화면 도중에 새로 생긴 카드는 늘이지 않는다(다음 세계 틱에 한 칸씩 움직임)
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_hr_sw,distance=..48] run function rlk:player/def/beat/st/tp1
