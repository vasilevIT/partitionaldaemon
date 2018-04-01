 select * from ( 
 select * from tracking_2018_4_1_8_48_7
 union all 
 select * from tracking_2018_4_1_8_48_8
 union all 
 select * from tracking_2018_4_1_8_48_9)
                where 
                time >= 1522561686.1784
                 and time <= 1522561689.1784