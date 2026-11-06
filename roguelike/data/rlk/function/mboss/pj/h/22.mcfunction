# Hit radius 2.2 b (+0.3 body), measured 0.9 b below the prop.
execute positioned ~ ~-0.9 ~ if entity @e[tag=rlk_body,distance=..2.5,limit=1] run function rlk:mboss/pj/hit
