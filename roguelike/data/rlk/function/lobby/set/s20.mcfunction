# 시점 바꾸기
# 1인칭 ↔ F5 위쪽 시점 (숄더뷰는 고르지 않음)
scoreboard players set #t lob 0
execute if score #on view matches 1 run scoreboard players set #t lob 1
execute if score #t lob matches 0 run function rlk:view/mode {m:2}
execute if score #t lob matches 1 run function rlk:view/off
# 시점이 바뀌며 클릭 감지 인터랙션이 다시 생기므로, 남은 클릭 신호를 지우고 잠깐 막음
execute as @e[tag=atkStrike] run data remove entity @s attack
execute as @e[tag=atkBlock] run data remove entity @s attack
scoreboard players set @s uiCd 20
function rlk:lobby/set/labels
