# stomp3/s1 Hydro (plan 4.6; call t5, launch t21, in flight to t27). As the body at the context
# point rotated to the player: the host group is kept for the launch (the next addon call may move it).
scoreboard players operation #axlBG mb = #azCtxGrp mb
scoreboard players set #azAftF mb 24
scoreboard players set #azAftD mb 16
function rlk:mboss/azhdaha/aft/new
