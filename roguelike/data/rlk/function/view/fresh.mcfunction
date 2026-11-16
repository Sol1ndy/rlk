# 시점 새로 시작 (@s = 플레이어): 서버를 다시 켜거나 다시 접속하면, 저장돼 있던 아바타·받침·조준 표식이
# 예전 상태(탑승·입력·위치)를 들고 남아 이동 입력이 엉뚱한 쪽으로 붙는다. 모두 지우고 다음 틱에 새로 만든다.
scoreboard players set #vFresh view 0
execute if entity @e[tag=rlk_view,limit=1] run function rlk:view/teardown
