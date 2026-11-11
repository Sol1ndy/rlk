# 박자의 끝(제 시간 · 다음 박자가 시작됨 · 사망 · 선택 공간 · 지도 · 연출 · /reload): 몇 번 불러도 같은 결과. 멈춘 것 · 기울인 것 · 늘인 것을
# 모두 되돌리고 표식을 지운다. 리그 캐릭터의 동작(클립)은 그대로 끝까지 가거나 플레이어의 다음 행동이 끊는다
scoreboard players set #btK cb 0
scoreboard players set #btA cb 0
scoreboard players set #btHold cb 0
scoreboard players set #btInv cb 0
scoreboard players operation #btAdj cb = #btLag cb
execute if score #btHeld cb matches 1 run function rlk:player/def/beat/hold_off
execute if score #btRk cb matches 1 run function rlk:player/def/beat/rock_off
execute if score #btSt cb matches 1 run function rlk:player/def/beat/st/off
execute if score #btTp cb matches 1 run function rlk:player/def/beat/st/tp_off
tag @e[tag=rlk_bt_atk] remove rlk_bt_atk
kill @e[type=minecraft:marker,tag=rlk_bt_pt]
execute as @a[tag=player] run attribute @s minecraft:movement_speed modifier remove rlk:beat_fov
execute as @a[tag=player,limit=1] run function rlk:char/motion/beat/off
