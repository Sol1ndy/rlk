# From rlk:tick while #mbLowG mb is 1 (@s = a player; before view/tick, so this tick's jump already uses it): low
# gravity on the player and on the shoulder-view avatar (view/move reads the avatar's own jump_strength):
# gravity x0.5, jump strength x1.19 (apex about 3 b, 25 t airtime), safe fall distance +4, all modifier
# rlk:mb_lowg. Multiplicative on purpose: the shoulder-view camera player has gravity base 0 and stays put.
# Re-added every tick (an existing modifier is not changed), so a re-created avatar gets it at once. The swing
# hold (jump x0, player/swing/tick) and every other x0 jump lock still win. Tag rlk_lowg marks who carries it.
function rlk:mboss/lowg_add
execute as @e[type=minecraft:mannequin,tag=rlk_av] run function rlk:mboss/lowg_add
