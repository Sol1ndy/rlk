# Short reposition, then guard II (after guard I) or chaos (after guard II).
function rlk:mboss/guardian/rig/face/track
execute if score #gdT mb < #gdGW mb run return 0
execute if score #gdGN mb matches 1 run return run function rlk:mboss/guardian/guard/begin2
function rlk:mboss/guardian/chaos/begin
