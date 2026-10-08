# 캐릭터별: 치유를 받기 직전 (@s = 플레이어, #heal tmp)
# 클로린드: 밤 순찰 중에 받는 치유는 생명의 계약으로 바뀐다(밤 꿰뚫기의 회복은 예외)
execute if score #charN tmp matches 4 if score @s clNV matches 1.. unless score #clHealOk tmp matches 1 run function rlk:char/clorinde/heal_to_bol
