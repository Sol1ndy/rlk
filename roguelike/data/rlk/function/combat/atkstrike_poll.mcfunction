# @s = 앞쪽 예비 입력 실드. 가까운 실드를 빗나간 입력도 같은 경로로 전달한다.
execute if data entity @s attack run function rlk:combat/input/poll_attack
execute if data entity @s interaction run function rlk:combat/input/poll_right
