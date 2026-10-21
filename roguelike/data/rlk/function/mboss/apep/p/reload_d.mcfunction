# GENERATED (reload): services resume through their reload; any other main-slot pattern is cancelled.
execute if score #apPid mb matches 40 run return run function rlk:mboss/apep/p/fail/reload
function rlk:mboss/apep/p/cancel
