# {id} (from room/rift/arm, @s = the zone marker of the new rift): the special's arena is forceloaded and its sliced
# build / look restore starts now (literal lines per special), long before the room is cleared (one arena job at a time:
# a chapter arena builds only on a boss map, which never rolls a rift). rlk:mboss sprep = the prepared special.
$data modify storage rlk:mboss sprep set value "$(id)"
$data modify storage rlk:mboss spg set value "$(id)"
execute if data storage rlk:mboss {spg:"spproto"} run return run function rlk:mboss/sp/pp/spproto
