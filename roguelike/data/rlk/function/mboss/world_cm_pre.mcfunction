# From mboss/world in a chapter fight (#mbMode 1), before the libraries and the module tick: out of bounds of the
# chapter arena (#mbAr >= 1; the plaza's is called by world directly), the body push request cleared (a per-tick
# request: set again by the module tick, cm.md 13.5), the lockv ring buffer (mv/lockv), proxy clicks polled.
execute if score #mbAr mb matches 1.. if score #mbOn mb matches 1 unless entity @a[tag=player,scores={devMode=1}] as @e[tag=rlk_body,limit=1] at @s run function rlk:mboss/ar/oob
scoreboard players set #mbPushOn mb 0
function rlk:mboss/mv/lv_sample
execute if score #mbPx mb matches 1 run function rlk:mboss/px/poll
