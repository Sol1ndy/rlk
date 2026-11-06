# Turn every Apep model passenger of @s (an organism husk) to its yaw (a tp would dismount them). @s = the husk.
execute rotated as @s on passengers if entity @s[tag=rlk_ap_om] run rotate @s ~ 0
