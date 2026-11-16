# 박자가 도는 동안 rlk:tick 의 뒤쪽(세계의 틱 · 아바타의 이동 뒤): 마네킹 캐릭터의 대역 리그 한 틱, 퍼펙트 닷지의 느린 화면에서 디스플레이
# 보간 늘이기(beat/st/*: 세계가 두 틱에 한 번 도는 동안(1~8틱; 세계 틱 = 0 · 2 · 4 · 6 · 8) 리그가 뚝뚝 끊기지 않고 1/2 속도로 이어 움직이게)
execute as @a[tag=player,limit=1] if score @s plActive matches 1 run function rlk:char/motion/lite/tick
execute unless score #btK cb matches 2 run return 0
execute unless score #btOn tmp matches 1 run return 0
execute if score #btA cb matches 0 run function rlk:player/def/beat/st/tp_on
execute if score #btA cb matches 0 run function rlk:player/def/beat/st/pass
execute if score #btA cb matches 2 run function rlk:player/def/beat/st/pass
execute if score #btA cb matches 4 run function rlk:player/def/beat/st/pass
execute if score #btA cb matches 6 run function rlk:player/def/beat/st/pass
execute if score #btA cb matches 6 run function rlk:player/def/beat/st/tp_off
execute if score #btA cb matches 8 run function rlk:player/def/beat/st/off
