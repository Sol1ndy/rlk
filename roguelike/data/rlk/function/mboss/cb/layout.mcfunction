# {id}: the domain-entrance layout of chapter boss <id> (F:room/cboss/<id>/layout, tools/build_cboss_rooms.py) into
# rlk:room cur; literal lines per boss (no $(id) in a function name). An unknown id falls back to Raiden's layout.
$data modify storage rlk:mboss cbl set value "$(id)"
function rlk:room/raiden/layout
