# @s = an emerging organism (apS 0): solid after the emergence; then the kind's first state.
execute if score @s apT matches ..9 run return 0
tag @s remove rlk_mb_inv
scoreboard players set @s apS 1
scoreboard players set @s apT 0
execute if score @s apK matches 1 run return run function rlk:boss/apep/org/basic/enter
execute if score @s apK matches 2 run return run function rlk:boss/apep/org/nurt/enter
execute if score @s apK matches 3 run return run function rlk:boss/apep/org/guard/enter
execute if score @s apK matches 4 run return run function rlk:boss/apep/org/nest/enter
execute if score @s apK matches 5 run return run function rlk:boss/apep/org/destr/enter
execute if score @s apK matches 6 run return run function rlk:boss/apep/org/pred/enter
