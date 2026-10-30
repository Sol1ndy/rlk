# The groggy re-offer (still debuffed after 달빛 해제): as many 달빛 이슬 as the cure meter still needs, one
# when one orb finishes it, else two (user: "하나만 먹어도 기믹 처리되는건 너무 쉬운 것 같아"; it used to be one).
execute as @a[tag=player,limit=1] run function rlk:mboss/butterfly/dew/need
scoreboard players operation #bfDew1 mb = #bfDewNeed mb
function rlk:mboss/butterfly/dew/offer
