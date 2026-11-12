# 느린 화면에 들어가는 틱(0틱, 그 틱의 이동 뒤): 틱마다 tp 로 움직이는 세계 쪽 디스플레이의 teleport_duration(1~19)을 2배로. 클라이언트는
# 이동 패킷을 길이보다 먼저 받으므로 한 틱 앞서 바꾼다(다음 이동 = 2틱)
scoreboard players set #btTp cb 1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_mb_part,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_mb_pj,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_raiden_part,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_cmlink,distance=..48] run function rlk:player/def/beat/st/tp1
execute at @e[tag=rlk_body,limit=1] as @e[type=#rlk:beat_disp,tag=rlk_cmp,distance=..48] run function rlk:player/def/beat/st/tp1
# 홍련의 칼이 지나온 자취(라운드 W: tools/mboss_scarlet/blade.py)의 그녀를 타는 카드는 rlk_mb_part 를 달아 위 줄이 함께 늘인다
# (라운드 V 의 rlk_hr_sw 줄은 그 카드가 없어져 지웠다: 레인 WB, 11-12)
