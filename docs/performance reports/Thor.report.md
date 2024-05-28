## Training Report - Random Forest Regressor

- **Model Identifier**: `MissingFive.joblib`


### Used dataset
car1.rec,car2.rec,car3.rec,car5.rec

### Features used
["angularVelocityX","angularVelocityY","angularVelocityZ","magneticFieldX","magneticFieldY","magneticFieldZ","accelerationX","accelerationY","accelerationZ","heading","pedal","voltage","distance"]

### (Live) Real-time testing results 
*(including out-of-sample data)*

| Car File | Turns within interval excl straights % | Track Direction |
|----------|----------------------------------------|-----------------|
| car1     | 49.70414201183432                      | CCW             |
| car2     | 67.90697674418604                      | CCW             |
| car3     | 62.077922077922075                     | CW              |
| car4     | 60.69651741293532                      | CW              |
| car5     | 60.36036036036037                      | CCW             |


Average performance: 60.144 (%)
