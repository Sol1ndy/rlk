# Both text lines from the current state (on every state, stage and meter change, and when the kit rebuilt
# its HUD components: #fkHudV, compared every module tick).
function rlk:mboss/fieldgen/hud/extra
function rlk:mboss/fieldgen/hud/sub
scoreboard players operation #fgHudV mb = #fkHudV mb
