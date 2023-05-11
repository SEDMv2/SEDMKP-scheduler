import pandas as pd
import numpy as np

ordered_altaz = []
azimuths = np.arange(0,351,10)
count = 0
for az in azimuths:
    for alt in np.arange(30,81,10):
        ordered_altaz.append(['point','999',f'point_{count}',count,az,alt,'2000',70.0,'cl'])
        count = count+1

df = pd.DataFrame(columns=["requester", "group_id", "object_id", "request_id", "az", "alt", "epoch",
                    "exposure_time","observation_choice"], data=ordered_altaz)
df.to_csv('fixed_schedule.csv',index=False)
