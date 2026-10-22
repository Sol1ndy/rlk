# 포식성: switch to the pod form now (body look pod, jaw and tail fin hidden). @s = the husk.
function rlk:boss/apep/om/pred/look/body/pod
execute on passengers if entity @s[tag=rlk_ap_om_jaw] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.05146f,-0.72f,-0.39668f],left_rotation:[0.02612f,0.06443f,-0.00169f,0.99758f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}
execute on passengers if entity @s[tag=rlk_ap_om_fin] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.14408f,-0.68f,-1.11069f],left_rotation:[0f,0.06445f,0f,0.99792f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}
