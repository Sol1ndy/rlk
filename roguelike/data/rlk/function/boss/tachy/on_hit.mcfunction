# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm known; scores only). G2: the mantle gauge;
# G3: the first reaction on her inside a core window flags the backfire (handled by the next fight tick).
execute if entity @s[tag=rlk_tk_mantle] run function rlk:boss/tachy/mantle/hit
execute if entity @s[tag=rlk_tk_core] if score #rx tmp matches 1.. if score #core tk matches 0 run scoreboard players set #core tk 2
