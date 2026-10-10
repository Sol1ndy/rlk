# @s = 눈 바로 앞 입력 실드. 좌클릭과 우클릭을 모두 소비한다.
execute if data entity @s attack run function rlk:combat/input/poll_attack
execute if data entity @s interaction run function rlk:combat/input/poll_right
