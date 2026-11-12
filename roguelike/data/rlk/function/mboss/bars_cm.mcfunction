# From mboss/bars in a chapter fight (#mbMode 1): after mboss/repool the new pool's bar refills over 30 t (#mbRamp);
# the bossui options (tools/build_bossbar.py), 0 = the default look, are reset before d/bars every call (cm.md 11):
# #buHpCol HP colour code, #buNoNum 1 = no numbers. (bossui/draw also resets both after every draw, so a mid-boss
# fight, which never sets them, and Raiden always draw the M0 line.)
execute if score #mbRamp mb matches 1.. run function rlk:mboss/bars_repool
scoreboard players set #buHpCol bu 0
scoreboard players set #buNoNum bu 0
