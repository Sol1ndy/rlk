# hr FN-f (mboss_lib.bars(0); any executor): the boss bars go and stay hidden until bars_on (#mbBarOff 1: mboss/world
# skips mboss/bars, the only re-show). fight_vars and cleanup_fight clear the flag.
scoreboard players set #mbBarOff mb 1
function rlk:mboss/bars_hide
