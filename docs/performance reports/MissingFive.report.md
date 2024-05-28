## Training Report - Random Forest Regressor

- **Model Identifier**: `Thor.joblib`


### Used dataset
car1.rec,car2.rec,car3.rec,car5.rec

### Features used
["angularVelocityX","angularVelocityY","angularVelocityZ","magneticFieldX","magneticFieldY","magneticFieldZ","accelerationX","accelerationY","accelerationZ","heading","pedal","voltage","distance"]

### (Live) Real-time testing results 
*(including out-of-sample data)*

| Car File | Turns within interval excl straights % | Track Direction |
|----------|----------------------------------------|-----------------|
| car1     | 44.97041420118343                      | CCW             |
| car2     | 63.0232558139535                       | CCW             |
| car3     | 56.62337662337662                      | CW              |
| car4     | 29.1044776119403                       | CW              |
| car5     | 57.65765765765766                      | CCW             |


Average performance: 50.324 (%)
