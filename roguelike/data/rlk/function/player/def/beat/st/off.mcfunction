# 느린 화면의 끝(8틱의 세계 틱 뒤, 또는 박자가 중간에 끝남): 늘여 둔 길이가 그대로 남은 디스플레이는 원래 길이로 되돌린다
scoreboard players set #btSt cb 0
scoreboard players set #btStN cb 0
execute as @e[tag=rlk_bt_st] run function rlk:player/def/beat/st/off1
