# Stand-in A8 judge (T + 194): shield/judge; the darkness lifts and the banner goes; a fail runs its branch.
function rlk:boss/scarlet/shield/judge
execute if score #gres hr matches 2 at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/ult/fail60
execute if score #gres hr matches 2 run function rlk:boss/scarlet/rig_stub/play/g_reform
