# From items/hook/on_heal, its first line (@s = player, #heal tmp >= 1), only while a fight is live (#mbLive 1).
# Every heal attempt counts as one heal event (#mbHealEv mb +1; the running module reads and clears it in its
# tick, e.g. the butterfly's 달빛 고치 cure meter), and the healing received is x #mbHealPct % (set by the module,
# 100 = unchanged; rounded half up), at least 1. #mbHealAmt mb adds up the amount after that factor (overheal
# included: the cap to max HP comes later in player/heal), cleared by the module with the events. It runs before
# the character hooks (Clorinde's Night Vigil turns heals into Bond of Life), so a heal that a character converts
# still counts and is reduced first.
scoreboard players add #mbHealEv mb 1
execute unless score #mbHealPct mb matches 100 run scoreboard players operation #heal tmp *= #mbHealPct mb
execute unless score #mbHealPct mb matches 100 run scoreboard players add #heal tmp 50
execute unless score #mbHealPct mb matches 100 run scoreboard players operation #heal tmp /= #c100 mb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
scoreboard players operation #mbHealAmt mb += #heal tmp
