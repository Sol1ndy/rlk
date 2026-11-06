# Mask hazard (kind 6, cm.md 13.6): hits a player whose feet are not within R0 + 0.3 b (horizontal) of any rlk_mb_hzsafe
# marker of its safe group; no radius limit; volley groups, #hzNoDodge, #hzRearm, the height band and NoRx as the other
# kinds; never drawn by the framework (the module / kit draws it). Options: #hzR0 mb = R0 (tenths), #hzSafeG mb = the
# safe group (0 = this hazard's own id mbHzI = #hzLast after the call). Safe markers: rlk_room rlk_mb_aux rlk_mb_hzsafe
# with mbHzSG = the group, made by the module after the call. Call: function rlk:mboss/hz/mask {tell:..,dmg:..}
scoreboard players set #hzR mb 0
scoreboard players set #hzK mb 6
$scoreboard players set #hzW mb $(tell)
$scoreboard players set #hzD mb $(dmg)
function rlk:mboss/hz/make
