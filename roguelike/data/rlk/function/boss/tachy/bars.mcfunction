# Hook bars (@s = body, every tick in intro / fight): the under-bar = the mantle gauge (gold) or the stun.
execute if score #pat tk matches 51 run function rlk:boss/tachy/hud/bar_gauge
execute if score #pat tk matches 52 if score #stun tk matches 1.. run function rlk:boss/tachy/hud/bar_stun
