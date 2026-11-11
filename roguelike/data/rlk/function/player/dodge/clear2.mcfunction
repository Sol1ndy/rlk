# player/dodge/clear: 끝나는 자리 근처에 적이 있으면 이번 틱의 이동 없이 동작의 마지막 틱으로
$execute at @e[tag=rlk_body,limit=1] positioned ~$(px) ~ ~$(pz) if entity @e[tag=rlk_mob,distance=..0.7] run return run function rlk:player/dodge/stop
