# 퍼펙트 패링의 박자, 실제 틱 #btA (beat/clock). 1~5 세계 멈춤 · 맞지 않음
scoreboard players set #btHold cb 0
execute if score #btOn tmp matches 1 if score #btA cb matches 1..5 run scoreboard players set #btHold cb 1
scoreboard players operation #btInv cb = #btHold cb
function rlk:player/def/beat/apply
execute if score #btA cb matches 1 at @e[type=minecraft:marker,tag=rlk_bt_pt,limit=1] run function rlk:player/def/fx/p3_boom
execute if score #btA cb matches 2 run function rlk:player/def/beat/p/a2
# round W(검토 T3-07: 낫이 3틱쯤 주황빛이다 어두워짐): 쳐내는 클립의 첫 프레임이 무기 모델을 제 모델로 다시 쓰므로 1 · 2틱에 빛나는 모델을 다시 씌운다
execute if score #btA cb matches 1..2 as @a[tag=player,limit=1] run function rlk:char/motion/beat/wglow_on
execute if score #btA cb matches 6 run function rlk:player/def/beat/p/a6
execute if score #btA cb matches 7..15 at @e[tag=rlk_bt_atk,limit=1] rotated ~ 0 run function rlk:player/def/fx/p3_bolt
execute if score #btA cb matches 12 as @a[tag=player,limit=1] run function rlk:char/motion/beat/wglow_off
execute if score #btA cb matches 17.. run function rlk:player/def/beat/end
