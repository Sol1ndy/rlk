# @s = body: the under-bar (plan 4.11): fight = mhpC - #mbFloor of the phase pool (Geo -> leg -> tail colour);
# transition = the step progress (gold); B3 tail window = time left (the tail colour).
execute if score #mbSt mb matches 0 run return 0
execute if score #azBur mb matches 1 run return run function rlk:mboss/azhdaha/hud/bar_b3
execute if score #azTr mb matches 2.. run return run function rlk:mboss/azhdaha/hud/bar_tr
function rlk:mboss/azhdaha/hud/bar_hp
