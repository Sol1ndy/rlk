# /function rlk:mboss/test/start {id:"proto"}: a real node map (chapter 1, map 2) whose kind-15 zone holds
# that mid-boss; the gate is pressed at once. Exercises roll -> gate -> arena -> fight -> won -> reward.
# {id:"help"}: the mid-boss ids (test/help_start).
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_start
$function rlk:mboss/test/start_ch {id:"$(id)",ch:1}
