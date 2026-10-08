# 판매 버튼: 처음 누르면 되묻고, 한 번 더 누르면 판다
execute if score @s pkSel matches -1 run return 0
execute unless score @s pkConf matches 1 run return run function rlk:invd/sell_ask
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
function rlk:invd/sell_do with storage rlk:lvpick a
