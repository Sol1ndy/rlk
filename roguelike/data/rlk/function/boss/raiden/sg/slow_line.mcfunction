# 「너무 느리군.」 on one blink in three.
execute store result score #rdSgR rd run random value 0..2
execute if score #rdSgR rd matches 0 run function rlk:boss/raiden/line/too_slow
