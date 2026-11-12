# Combat overhaul C (rlk:tick right after mboss/main, only while the perfect-dodge window is open and the fight is live and
# not paused: #dgOpen cb 1, the dodge started this tick or the 2 before, so the body has already moved 1-3 b): every dodgeable hazard in its active window that did not hit and
# every dodgeable prop that did not hit is tested once more at the dodge's start (hz/near, pj/near): a contact there is
# judged as a perfect dodge (never damage).
execute if score #mbHzOn mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_hz] at @s rotated as @s run function rlk:mboss/hz/near
execute if score #mbPjOn mb matches 1 as @e[tag=rlk_mb_pj] at @s rotated as @s run function rlk:mboss/pj/near
