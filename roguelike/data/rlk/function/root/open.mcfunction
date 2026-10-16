# 나무뿌리를 누름 (@s = 플레이어, at @s, #rootG room = 그 오브젝트의 ogid). 각인 셋 중 하나를 고르는 화면(pkMode 7)
execute if score @s pkMode matches 1.. run return 0
execute if score #mirUsed room matches 1.. run return run function rlk:char/deny {t:"세계수의 기적은 한 판에 한 번뿐입니다"}
# 선택지는 나무뿌리 하나당 한 번만 정한다(나갔다 와도 같음)
execute unless score #rootRolled room = #rootG room run function rlk:root/roll
# 업데이트 전에 정해 둔 선택지에는 아이템이 없으니 지금 정한다
execute unless data storage rlk:room rooti run function rlk:root/roll_items
function rlk:lvup/enter {mode:7}
