# 무리 베기는 한 틱에 한 번만 맞힘(여러 마리가 같은 틱에 베도 15 한 번)
scoreboard players set #c2NsHit tmp 1
scoreboard players operation #cmDmg tmp = #c2D_ns tmp
function rlk:cm/hit_me
