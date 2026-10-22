# Hook aux_hit (@s = an aux inside combat/apply, #dmg after RES; cm.md 8): the 양육 immunity (U2, "buffed
# organisms can't be damaged"; NURTURE_MODE A: AP-REV tags the immune organism rlk_mb_ap_imm): #dmg 0 ->
# aux/take shows "면역" and takes nothing. Otherwise the organism runtime (shield pools, ...: org/aux_hit).
execute if entity @s[tag=rlk_mb_ap_imm] run return run scoreboard players set #dmg tmp 0
function rlk:boss/apep/org/aux_hit
