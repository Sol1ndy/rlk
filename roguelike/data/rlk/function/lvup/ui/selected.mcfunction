# 고른 아이템을 크게 (누를 수 없음)
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
function rlk:lvup/ui/selected2 with storage rlk:lvpick a
