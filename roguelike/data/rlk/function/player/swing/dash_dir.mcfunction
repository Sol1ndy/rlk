# 1인칭 대쉬 방향 (@s = 플레이어, at 몸 = 플레이어, player/dash_dir 에서 휘두르는 중(swHold)일 때만).
# 휘두르는 동안은 몸이 서 있어 지난 틱의 이동량이 0이므로, 숄더뷰(view/dash_dir)처럼 누르고 있는 이동 키 방향으로 대쉬한다.
# 아무 키도 누르지 않았으면 그대로 둔다(시선 방향 또는 넉백으로 밀린 방향).
scoreboard players set #swF tmp 0
scoreboard players set #swS tmp 0
execute if predicate rlk:in_f run scoreboard players add #swF tmp 1
execute if predicate rlk:in_b run scoreboard players remove #swF tmp 1
execute if predicate rlk:in_l run scoreboard players add #swS tmp 1
execute if predicate rlk:in_r run scoreboard players remove #swS tmp 1
execute if score #swF tmp matches 0 if score #swS tmp matches 0 run return 0
kill @e[tag=rlk_dashmk]
execute if score #swF tmp matches 1 if score #swS tmp matches 0 rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches 1 if score #swS tmp matches 1 rotated ~-45 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches 0 if score #swS tmp matches 1 rotated ~-90 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches -1 if score #swS tmp matches 1 rotated ~-135 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches -1 if score #swS tmp matches 0 rotated ~180 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches -1 if score #swS tmp matches -1 rotated ~135 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches 0 if score #swS tmp matches -1 rotated ~90 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute if score #swF tmp matches 1 if score #swS tmp matches -1 rotated ~45 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute store result score #dvx tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[0] 100
execute store result score #dvz tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[2] 100
kill @e[tag=rlk_dashmk]
scoreboard players operation #dvx tmp -= #cx tmp
scoreboard players operation #dvz tmp -= #cz tmp
scoreboard players set #amove tmp 100
