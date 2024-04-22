## Training Report - Random Forest Regressor

- **Model Identifier**: `Toyota.joblib`
- **Feature Scaler Identifier**: `Toyota-feature.joblib`
- **Target Scaler Identifier**: `Toyota-target.joblib`

### Used dataset
car.rec, car2.rec,car3.rec,car4.rec,car5.rec,car5.rec

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

| Car File | Turns within interval (%) | Track Direction |
|----------|---------------------------|-----------------|
| car1     | 68.6                      | CW              |
| car2     | 40.7                      | CCW             |
| car3     | 57.7                      | CCW             |
| car4     | 66.9                      | CW              |
| car5     | 57.6                      | CW              |
| car6     | 54.3                      | CCW             |

