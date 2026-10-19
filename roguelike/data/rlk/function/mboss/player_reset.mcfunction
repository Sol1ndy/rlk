# Player-side fight modifiers back to neutral (fight start, cleanup_fight): healing received 100 %, no crit
# chance / crit damage change, no pending heal events or amounts, no low gravity. The player's crit stats are
# recomputed every 2 t (items/stat_light -> items/hook/stat_buffs).
scoreboard players set #mbHealPct mb 100
scoreboard players set #mbCritAdd mb 0
scoreboard players set #mbCritDmgAdd mb 0
scoreboard players set #mbHealEv mb 0
scoreboard players set #mbHealAmt mb 0
# low gravity off (rlk:tick removes the modifiers on the next tick: mboss/lowg_off)
scoreboard players set #mbLowG mb 0
