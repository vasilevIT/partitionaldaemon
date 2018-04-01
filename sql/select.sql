 select * from ( 
 select * from tracking_2018_4_1_7_19_0
 union all 
 select * from tracking_2018_4_1_7_19_1
 union all 
 select * from tracking_2018_4_1_7_19_2)
                where 
                time >= 1522556339.674518
                 and time <= 1522556342.674518