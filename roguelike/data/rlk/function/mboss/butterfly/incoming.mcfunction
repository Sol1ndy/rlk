# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). NO element RES of any
# kind (user decision "불, 풀 내성은 없애줘"): mres stays 0 and nothing here reads #elem. Only the player's
# 달빛 고치 (DMG 50 %, forced crits undone: CRIT -100 %) and 달빛 축복 받음 (DMG 150 %), reactions included.
execute if score #bfCoc mb matches 1 if score #crit tmp matches 1 run function rlk:mboss/butterfly/coc/uncrit
execute unless score #bfDmgPct mb matches 100 if score #dmg tmp matches 1.. run function rlk:mboss/butterfly/coc/dmg
