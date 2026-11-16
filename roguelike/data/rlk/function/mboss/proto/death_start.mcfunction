# Hook death_start (@s = body, hazards already cleared, bars hidden).
scoreboard players set #prPat mb 0
kill @e[tag=rlk_mb_proto_star]
kill @e[tag=rlk_mb_proto_starv]
kill @e[tag=rlk_mb_proto_jav]
function rlk:mboss/proto/rig/unglow
function rlk:mboss/proto/pose/death {d:14}
function rlk:mboss/line/say {t:"...여기까지인가.",c:"#E8C890",gap:2,hold:36,snd:2}
