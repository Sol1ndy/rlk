# From items/hook/on_heal, its first line (@s = player, #heal tmp >= 1), only while a fight is live (#mbLive 1).
# Every heal attempt counts as one heal event (#mbHealEv mb +1; the running module reads and clears it in its
# tick, e.g. the butterfly's 달빛 고치 cure), and the healing received is x #mbHealPct % (set by the module,
# 100 = unchanged), at least 1. It runs before the character hooks (Clorinde's Night Vigil turns heals into
# Bond of Life), so a heal that a character converts still counts and is reduced first.
scoreboard players add #mbHealEv mb 1
execute if score #mbHealPct mb matches 100 run return 0
scoreboard players operation #heal tmp *= #mbHealPct mb
scoreboard players operation #heal tmp /= #c100 mb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
