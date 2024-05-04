## Training Report - Random Forest Classifier

- **Model Identifier**: `Hildegard.joblib`
- **Feature Scaler Identifier**: `Hildegard-feature.joblib`
- **Target Scaler Identifier**: `Hildegard-target.joblib`

### Used dataset
car.rec,car2.rec,car3.rec,car4.rec,car5.rec,car6.rec

### Targets
This model is a wheel state binary classification model and has the responsibility
of deciding whether or not the car is turning or not. If it is turning the data is passed
to our regression models

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
*(including straights)*

| Car File | Correctly predicted wheel states (%) | Track Direction |
|----------|--------------------------------------|-----------------|
| car1     | 97.10                                | CW              |
| car2     | 87.88                                | CCW             |
| car3     | 89.46                                | CCW             |
| car4     | 96.84                                | CW              |
| car5     | 89.34                                | CW              |
| car6     | 93.56                                | CCW             |

Average performance: 92,36 (%)