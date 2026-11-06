# A hit taken while the player stands behind her (> 120 deg off her facing, <= 8 b): remember it for 40 t.
function rlk:boss/raiden/sg/rear_test
execute if score #rdSgRear rd matches 1 run scoreboard players set @s rdSgRearT 40
