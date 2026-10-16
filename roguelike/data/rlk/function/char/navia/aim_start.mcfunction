# 조준 시작 (@s = 플레이어, at 몸): 움직일 수 없음(+ 화면 확대) · 우산총 · 조준 모션 "skill_aim_in" → "skill_aim"(반복)
scoreboard players set @s nvA 1
scoreboard players set @s nvGap 0
scoreboard players set @s dashMoveT 0
attribute @s minecraft:movement_speed modifier remove rlk:navia_aim
attribute @s minecraft:movement_speed modifier add rlk:navia_aim -1 add_multiplied_total
attribute @s minecraft:jump_strength modifier remove rlk:navia_aim
attribute @s minecraft:jump_strength modifier add rlk:navia_aim -1 add_multiplied_total
function rlk:view/stop_h
kill @e[tag=rlk_nvopen]
# 블록 우산총은 1인칭에서만(숄더뷰는 모션의 우산 모델)
execute unless score @s pmVisible matches 1 run function rlk:char/navia/gun_spawn
# 조준 시작 소리(게임 쪽이 소유: 모션 소리 skill_aim_in 에 같은 소리를 넣지 않는다)
execute unless score #k223 snd matches 1 run function rlk:snd/f247
execute unless score #k224 snd matches 1 run function rlk:snd/f248
function rlk:char/motion/start {char:"navia",clip:"skill_aim_in"}
