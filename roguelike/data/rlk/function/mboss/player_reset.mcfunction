# Player-side fight modifiers back to neutral (fight start, cleanup_fight): healing received 100 %, no crit
# change, no pending heal events, no low gravity. The player's crit chance is recomputed every 2 t (items/stat_light).
scoreboard players set #mbHealPct mb 100
scoreboard players set #mbCritAdd mb 0
scoreboard players set #mbHealEv mb 0
# low gravity off (rlk:tick removes the modifiers on the next tick: mboss/lowg_off)
scoreboard players set #mbLowG mb 0
