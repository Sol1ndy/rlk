# The player received a heal this tick or the last (rlk:mboss/player_heal counted it; the heal itself was already
# reduced to 60 %): ANY heal cures 달빛 고치 (user decision; not only a full heal).
scoreboard players set #mbHealEv mb 0
execute if score #bfCoc mb matches 1 run function rlk:mboss/butterfly/coc/cure
