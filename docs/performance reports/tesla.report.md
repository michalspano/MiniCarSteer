## Training Report - Random Forest Regressor

- **Model Identifier**: `Tesla.joblib`
- **Feature Scaler Identifier**: `Tesla-feature.joblib`
- **Target Scaler Identifier**: `Tesla-target.joblib`

### Used dataset
car.rec, car2.rec,car3.rec,car4.rec,car5.rec,car6.rec

### Features used and reasoning for use
#### Acceleration Y axis
When the car turns the acceleration on the Y axis will change because of centripetal force. This change is relevant for us, and especially in ensemble learning.

#### Magnetic Field Z axis
This feature has previously shown a non-linear relationship between its value and steering angle when used on its own in the random forest model. 

#### Heading (true north)
When the car turns the direction that the car is facing will change, hence the position of north relative to the car will change too. This change is relevant for deriving steering angle.

#### Angular velocity Z axis
This feature has previously shown a linear relationship between its value and steering angle when used on its own in the random forest model.

### (Live) Real-time testing results 
*(including out-of-sample data)*

| Car File | Turns within interval excl straights % | Track Direction |
|----------|----------------------------------------|-----------------|
| car1     | 63.85                                  | CW              |
| car2     | 33.93                                  | CCW             |
| car3     | 51.52                                  | CCW             |
| car4     | 64.23                                  | CW              |
| car5     | 51.27                                  | CW              |
| car6     | 51.03                                  | CCW             |


Average performance: 52.64 (%)
