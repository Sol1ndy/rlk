# Macro {i}, at footprint i: the dome forms: the safe marker (rlk_mb_ap_dome + rlk_mb_hzsafe, mbHzSG = the cast's group;
# at the floor point, RFX-3 / RORG-2), the dome models (org om/dome, rising), the rise sparkle and its sound.
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p32","rlk_mb_ap_dome","rlk_mb_hzsafe","rlk_mb_ap_p32n"]}
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_p32n] mbHzSG = #apq32G mb
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_p32n] apL $(i)
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p32n] remove rlk_mb_ap_p32n
$execute rotated 0 0 run function rlk:boss/apep/om/dome/spawn {i:$(i)}
$function rlk:boss/apep/om/dome/play {i:$(i),clip:"dome_rise"}
function rlk:boss/apep/fx/p/dome_rise
function rlk:boss/apep/fx/snd/q2_dome
