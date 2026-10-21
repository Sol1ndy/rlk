# A 180-degree crab-turn (service 10, kind 4: two steps toward the player's side).
scoreboard players set #apBackN mb 0
scoreboard players set #apMvK mb 4
scoreboard players set #apPick mb 10
function rlk:mboss/apep/ai/go_raw
return 1
