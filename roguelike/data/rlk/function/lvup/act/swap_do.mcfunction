# 교체 확인: 그 아이템을 내려놓고(돌아갈 때 발밑에 놓임) 고른 아이템을 얻는다
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
execute store result storage rlk:lvpick a.j int 1 run scoreboard players get @s pkSwap
function rlk:lvup/act/swap2 with storage rlk:lvpick a
