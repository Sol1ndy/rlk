# {s}: the stand-in cut at its lock (@s = body): a marker rlk_hr_cut at the player's feet registers the pip
# window of strike s (shield/cut as the marker, at it); it goes 2 t after the strike.
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_cut","rlk_hr_gsnew"]}
$execute as @e[type=minecraft:marker,tag=rlk_hr_gsnew,limit=1] at @s run function rlk:boss/scarlet/shield/cut {s:$(s)}
tag @e[type=minecraft:marker,tag=rlk_hr_gsnew] remove rlk_hr_gsnew
