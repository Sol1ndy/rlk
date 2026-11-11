# FN-cam: the hand-back (@s = a player; a no-op unless they carry the hold tag, so it is idempotent). Called by rlk:tick
# when the request has stopped (a sequence's end / cancel / skip to an unlocked state, a pause: death, Ronova's revive,
# the selection screen, a missing player or body), by mboss/cam/hold (no fight, the live stand gone), by cleanup_fight
# (won, cancelled, cleanup, abort, the tests, uninstall) and by mboss/init (/reload); a player who logged out held is
# released by rlk:tick in their first tick back. Un-spectate, the stored game mode, back to the avatar's place facing
# the boss, on the F5 seat again; the cinematic actor goes and the avatar shows (char/cine/stop, when lane H3's exists).
execute unless entity @s[tag=rlk_mb_camh] run return 0
tag @s remove rlk_mb_camh
execute if entity @s[gamemode=spectator] run spectate
execute if entity @s[tag=rlk_mb_cgS] run gamemode survival @s
execute if entity @s[tag=rlk_mb_cgC] run gamemode creative @s
execute unless entity @s[tag=rlk_mb_cgS] unless entity @s[tag=rlk_mb_cgC] run gamemode adventure @s
tag @s remove rlk_mb_cgS
tag @s remove rlk_mb_cgC
# dead / in the selection space: those own the player's place (as view/teardown)
execute unless score @s pkMode matches 1.. unless score @s dead matches 1 run function rlk:mboss/cam/back
data remove storage rlk:mboss camret
function rlk:char/cine/stop
