# Hook resume (@s = body): patterns with a resume hook (S4); during the mantle the cocoon card again (pause
# cleared the kit cards; the gauge redraws it), during the nova the rest of its swell (S4 p/mantle/nova/resume).
execute if score #pat tk matches 8 run function rlk:boss/tachy/p/k/resume
execute if score #pat tk matches 9 run function rlk:boss/tachy/p/w1/resume
execute if score #pat tk matches 10 run function rlk:boss/tachy/p/w2/resume
execute if score #pat tk matches 51 run scoreboard players set #hud_c tk -1
execute if score #pat tk matches 51 run function rlk:boss/tachy/mantle/gauge
execute if score #pat tk matches 53 run function rlk:boss/tachy/p/mantle/nova/resume
