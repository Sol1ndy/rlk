# @s = a bolt at the Heart: the Heart loses (buffed -120), the hit sound, gone.
execute if entity @s[tag=rlk_mb_ap_bbuf] run function rlk:boss/apep/heart/sub {v:108}
execute unless entity @s[tag=rlk_mb_ap_bbuf] run function rlk:boss/apep/heart/sub {v:54}
function rlk:boss/apep/fx/snd/o2_hit
kill @s
