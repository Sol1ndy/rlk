# 아이템을 누름: 고른 것이 없으면 고르고, 같은 것이면 풀고, 다른 것이면 두 아이템의 자리를 바꾼다
execute if score @s pkSel matches -1 run return run function rlk:invd/select
execute if score @s pkSel = @s pkHI run return run function rlk:invd/deselect
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
execute store result storage rlk:lvpick a.j int 1 run scoreboard players get @s pkHI
function rlk:invd/swap with storage rlk:lvpick a
