# @s = 플레이어. 인챈트 화면 열기 (가진 아이템이 있어야 함)
execute if score @s pkMode matches 1.. run return 0
execute if score #enchN room matches ..0 run return 0
execute unless data storage rlk:pinv order[0] run return run function rlk:char/deny {t:"강화할 아이템이 없습니다"}
function rlk:lvup/enter {mode:8}
