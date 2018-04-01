 create view tracking_1 as  
 select * from tracking_2018_4_1_7_18_56
union all  
 select * from tracking_2018_4_1_7_18_57
union all  
 select * from tracking_2018_4_1_7_18_58
union all  
 select * from tracking_2018_4_1_7_18_59
union all  
 select * from tracking_2018_4_1_7_19_0
union all  
 select * from tracking_2018_4_1_7_19_1
union all  
 select * from tracking_2018_4_1_7_19_2
union all  
 select * from tracking_2018_4_1_7_19_3
union all  
 select * from tracking_2018_4_1_7_19_4
union all  
 select * from tracking_2018_4_1_7_19_5 create view tracking as 
 select * from tracking_1