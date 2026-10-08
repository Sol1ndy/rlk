# 부활 직후 (@s = 플레이어): 지금 서버가 알고 있는 입력 상태를 "믿을 수 없는 상태"로 적어 둔다. 아무 키도 안 눌린 상태면 할 일 없음
scoreboard players set #inM view 0
execute if predicate rlk:in_f run scoreboard players add #inM view 1
execute if predicate rlk:in_b run scoreboard players add #inM view 2
execute if predicate rlk:in_l run scoreboard players add #inM view 4
execute if predicate rlk:in_r run scoreboard players add #inM view 8
execute if predicate rlk:in_jump run scoreboard players add #inM view 16
execute if predicate rlk:in_sprint run scoreboard players add #inM view 32
scoreboard players operation #inBase view = #inM view
scoreboard players set #inStale view 0
execute if score #inM view matches 1.. run scoreboard players set #inStale view 1
# 아바타에 남은 속도도 지운다
execute as @e[tag=rlk_av,limit=1] run data modify entity @s Motion set value [0.0d,0.0d,0.0d]
