# The opener ended: its host (#apNext) starts now (no opener check, no recover).
scoreboard players operation #apPick mb = #apNext mb
scoreboard players set #apNext mb 0
function rlk:mboss/apep/ai/go_raw
