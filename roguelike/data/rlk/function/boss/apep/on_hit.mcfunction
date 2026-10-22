# Hook on_hit (@s = body inside combat/apply; #elem #dmg known; RES already from mres = mbRes<#elem>, cm.md 8):
# the flash group of the hit proxy (#mbPart, cm.md 9.5; 0 = a direct body hit -> the body group).
scoreboard players operation #apFlash mb = #mbPart mb
