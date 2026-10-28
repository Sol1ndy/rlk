execute positioned as @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^2.5 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~
execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~ ~ #rlk:dash_pass run return 0
execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~0.5 ~ #rlk:dash_pass run return 0
function rlk:cm/ci/orbit_go
