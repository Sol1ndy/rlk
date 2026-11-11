# FN-cam: the F5 seat again at the avatar (the execution position), as view/seat_new makes it (its lines, read at
# build time) without the "press F5" chat hint: the hold removed the seat, the hand-back needs it in the same tick.
summon minecraft:armor_stand ~ ~ ~ {Tags:["rlk_view","rlk_vseat","rlk_pet"],Small:1b,Invisible:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,NoBasePlate:1b,DisabledSlots:4144959}
ride @e[tag=rlk_vseat,limit=1] mount @e[tag=rlk_av,limit=1]
function rlk:view/ride_apply
