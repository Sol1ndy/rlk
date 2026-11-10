# hr_design §1.5: a perfect parry on the running pattern's last / single hit (@s = body; the pattern's PP window): she
# flinches (clip flinch) and the pattern ends 6 t later (core/ppf instead of its tick).
execute if score #ppf hr matches 1.. run return 0
scoreboard players set #ppf hr 6
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/rig/play/flinch
