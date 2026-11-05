# {s}: the lock of the cut of strike s (strike - LOCK_LEAD 7): the last aim; from now on it stays. A counting cut
# registers its pip window at this point (S3's shield/cut {s}, as the cut marker, at it).
$function rlk:boss/scarlet/g/cut/aim {s:$(s)}
$execute as @e[type=minecraft:marker,tag=rlk_hr_cnt,scores={hr=$(s)},limit=1] at @s run function rlk:boss/scarlet/shield/cut {s:$(s)}
