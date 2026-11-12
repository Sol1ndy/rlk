# straight up by #oUp/100 b if open and under the ceiling
execute unless function rlk:cm/rv/below_cap run return 0
execute positioned ~ ~0.3 ~ if function rlk:cm/rv/free run tp @s ~ ~ ~
