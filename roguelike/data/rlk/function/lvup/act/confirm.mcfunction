# 확인: 인벤(9칸)에 자리가 있으면 바로 획득, 가득 찼으면 바꿀 아이템을 고르게 한다
# 캐릭터를 골랐으면: 보유 칸과 상관없이 바로 교체
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
function rlk:lvup/act/char_chk with storage rlk:lvpick a
execute if score #pkIsChar tmp matches 1 run return run function rlk:lvup/act/char_take
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp matches 9.. run return run function rlk:lvup/act/to_swap
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
function rlk:lvup/act/give with storage rlk:lvpick a
function rlk:lvup/act/resolve
