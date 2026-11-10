# GENERATED: return 1 when the running boss (#mbId mb) has the balance gauge (registry "bal", rlk:bal/init).
execute if score #mbId mb matches 1 run return 1
execute if score #mbId mb matches 2 run return 1
execute if score #mbId mb matches 3 run return 1
execute if score #mbId mb matches 99 run return 1
execute if score #mbId mb matches 98 run return 1
execute if score #mbId mb matches 10 run return 1
execute if score #mbId mb matches 11 run return 1
execute if score #mbId mb matches 20 run return 1
execute if score #mbId mb matches 97 run return 1
execute if score #mbId mb matches 12 run return 1
execute if score #mbId mb matches 21 run return 1
return fail
