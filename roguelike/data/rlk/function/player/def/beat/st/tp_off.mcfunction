# 느린 화면의 마지막 느린 세계 틱 뒤(6틱; 다음 이동 = 8틱은 제 길이), 또는 박자가 중간에 끝남: teleport_duration 을 되돌린다
scoreboard players set #btTp cb 0
execute as @e[tag=rlk_bt_tp] run function rlk:player/def/beat/st/tp_off1
