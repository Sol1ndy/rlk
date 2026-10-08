# @s = 플레이어(숄더뷰). 대쉬 방향을 입력 방향으로 바꿔치기: #amove 를 0(시선 방향) 또는 100(이동 방향 #dvx,#dvz)으로
scoreboard players set #amove tmp 0
execute if score #inAct view matches 1 run scoreboard players set #amove tmp 100
execute if score #inAct view matches 1 run scoreboard players operation #dvx tmp = #inx view
execute if score #inAct view matches 1 run scoreboard players operation #dvz tmp = #inz view
