#include <Arduino.h>

/*****************************************************************

This Arduino sketch is a demo of the simple side of the
SFE_LSM9DS1 library. It'll demo the following:
* How to create a LSM9DS1 object, using a constructor (global
  variables section).
* How to use the begin() function of the LSM9DS1 class.
* How to read the gyroscope, accelerometer, and magnetometer
  using the readGryo(), readAccel(), readMag() functions and
  the gx, gy, gz, ax, ay, az, mx, my, and mz variables.
* How to calculate actual acceleration, rotation speed,
  magnetic field strength using the calcAccel(), calcGyro()
  and calcMag() functions.
* How to use the data from the LSM9DS1 to calculate
  orientation and heading.

Hardware setup: This library supports communicating with the
LSM9DS1 over either I2C or SPI. This example demonstrates how
to use I2C. The pin-out is as follows:
  LSM9DS1 --------- Arduino
   SCL ---------- SCL (A5 on older 'Duinos')
   SDA ---------- SDA (A4 on older 'Duinos')
   VDD ------------- 3.3V
   GND ------------- GND
(CSG, CSXM, SDOG, and SDOXM should all be pulled high.
Jumpers on the breakout board will do this for you.)

The LSM9DS1 has a maximum voltage of 3.6V. Make sure you power it
off the 3.3V rail! I2C pins are open-drain, so you'll be
(mostly) safe connecting the LSM9DS1's SCL and SDA pins
directly to the Arduino.*/
// The SFE_LSM9DS1 library requires both Wire and SPI be
// included BEFORE including the 9DS1 library.
#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <SoftwareSerial.h> //Serial library

//////////////////////////
// LSM9DS1 Library Init //
//////////////////////////
// Use the LSM9DS1 class to create an object. [imu] can be
// named anything, we'll refer to that throught the sketch.
LSM9DS1 imu;
SoftwareSerial bt (2,3);  //RX, TX (Switched on the Bluetooth - RX -> TX | TX -> RX)

///////////////////////
// Example I2C Setup //
///////////////////////
// SDO_XM and SDO_G are both pulled high, so our addresses are:
#define LSM9DS1_M 0x1E // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG  0x6B // Would be 0x6A if SDO_AG is LOW

////////////////////////////
// Sketch Output Settings //
////////////////////////////
#define PRINT_CALCULATED
//#define PRINT_RAW
#define PRINT_SPEED 500 // 1000 ms between prints
static unsigned long lastPrint = 0; // Keep track of print time

// Earth's magnetic field varies by location. Add or subtract
// a declination to get a more accurate heading. Calculate
// your's here:
// http://www.ngdc.noaa.gov/geomag-web/#declination
#define DECLINATION -10 // Declination (degrees) in Boulder, CO.
float gyro_angle = 0;
float gyro_x_cal, gyro_y_cal, gyro_z_cal;//those will account for gyro drift hopefully

void setup()
{
  bt.begin(9600); //Open the serial port
  Serial.begin(115200);

  // Before initializing the IMU, there are a few settings
  // we may need to adjust. Use the settings struct to set
  // the device's communication mode and addresses:
  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;
  // The above lines will only take effect AFTER calling
  // imu.begin(), which verifies communication with the IMU
  // and turns it on.
  if (!imu.begin())
  {
    bt.println("Failed to communicate with LSM9DS1.");
    bt.println("Double-check wiring.");
    bt.println("Default settings in this sketch will " \
                  "work for an out of the box LSM9DS1 " \
                  "Breakout, but may need to be modified " \
                  "if the board jumpers are.");
    while (1)
      ;
  }
  for (int cal_int = 0; cal_int < 1000 ;cal_int++ ){
    if ( imu.gyroAvailable() ) {                //Read the raw acc and gyro data from the MPU-6050 for 1000 times
      imu.readGyro();
      //cal_int++;
    }
    gyro_x_cal += imu.calcGyro(imu.gx);                                              //Add the gyro x offset to the gyro_x_cal variable
    gyro_y_cal += imu.calcGyro(imu.gy);                                              //Add the gyro y offset to the gyro_y_cal variable
    gyro_z_cal += imu.calcGyro(imu.gz);                                              //Add the gyro z offset to the gyro_z_cal variable
    delay(3);                                                          //Delay 3us to have 250Hz for-loop
  }

  // divide by 1000 to get avarage offset
  gyro_x_cal /= 1000;
  gyro_y_cal /= 1000;
  gyro_z_cal /= 1000;

    imu.calibrate();         //calibrates but does not store bias
    imu.calibrateMag();       //calibrates and stores bias
}


void printGyro()
{
  // Now we can use the gx, gy, and gz variables as we please.
  // Either print them as raw ADC values, or calculated in DPS.
  //bt.print("G: ");
#ifdef PRINT_CALCULATED
  // If you want to print calculated values, you can use the
  // calcGyro helper function to convert a raw ADC value to
  // DPS. Give the function the value that you want to convert.
 // bt.print(imu.calcGyro(imu.gx), 2);
  //bt.print(", ");
  //bt.print(imu.calcGyro(imu.gy), 2);
  //bt.print(", ");
  //bt.print(imu.calcGyro(imu.gz), 2);
  //bt.println(" deg/s");

  gyro_angle+=imu.calcGyro(imu.gz)-gyro_z_cal;//assuming one second passed
  //bt.print(gyro_angle);

#elif defined PRINT_RAW
  bt.print(imu.gx);
  bt.print(", ");
  bt.print(imu.gy);
  bt.print(", ");
  bt.println(imu.gz);
#endif
}

void printAccel()
{
  // Now we can use the ax, ay, and az variables as we please.
  // Either print them as raw ADC values, or calculated in g's.
  bt.print("A: ");
#ifdef PRINT_CALCULATED
  // If you want to print calculated values, you can use the
  // calcAccel helper function to convert a raw ADC value to
  // g's. Give the function the value that you want to convert.
  bt.print(imu.calcAccel(imu.ax), 2);
  bt.print(", ");
  bt.print(imu.calcAccel(imu.ay), 2);
  bt.print(", ");
  bt.print(imu.calcAccel(imu.az), 2);
  bt.println(" g");
#elif defined PRINT_RAW
  bt.print(imu.ax);
  bt.print(", ");
  bt.print(imu.ay);
  bt.print(", ");
  bt.println(imu.az);
#endif

}

void printMag()
{
  // Now we can use the mx, my, and mz variables as we please.
  // Either print them as raw ADC values, or calculated in Gauss.
  bt.print("M: ");
#ifdef PRINT_CALCULATED
  // If you want to print calculated values, you can use the
  // calcMag helper function to convert a raw ADC value to
  // Gauss. Give the function the value that you want to convert.
  bt.print(imu.calcMag(imu.mx), 2);
  bt.print(", ");
  bt.print(imu.calcMag(imu.my), 2);
  bt.print(", ");
  bt.print(imu.calcMag(imu.mz), 2);
  bt.println(" gauss");
#elif defined PRINT_RAW
  bt.print(imu.mx);
  bt.print(", ");
  bt.print(imu.my);
  bt.print(", ");
  bt.println(imu.mz);
#endif
}

// Calculate pitch, roll, and heading.
// Pitch/roll calculations take from this app note:
// http://cache.freescale.com/files/sensors/doc/app_note/AN3461.pdf?fpsp=1
// Heading calculations taken from this app note:
// http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/Magnetic__Literature_Application_notes-documents/AN203_Compass_Heading_Using_Magnetometers.pdf
void printAttitude(float ax, float ay, float az, float mx, float my, float mz)
{

 
   //pitch = atan2 (accelY ,( sqrt ((accelX * accelX) + (accelZ * accelZ))));
   //roll = atan2(-accelX ,( sqrt((accelY * accelY) + (accelZ * accelZ))));




    //roll = roll*57.3;
    //pitch = pitch*57.3;
    //yaw = yaw*57.3;



  float yaw;
  float pitch = atan2(ay, sqrt(ax*ax+az*az));
  float roll = atan2(-ax, sqrt(ay * ay + az * az));

   // yaw from mag

   float Yh = (my * cos(roll)) - (mz * sin(roll));
   float Xh = (mx * cos(pitch))+(my * sin(roll)*sin(pitch)) + (mz * cos(roll) * sin(pitch));

   yaw =  atan2(Yh, Xh);

  float heading;
  if (my == 0)
    heading = (mx < 0) ? PI : 0;
  else
    heading = atan2(mx, my);

  heading -= DECLINATION * PI / 180;

  if (heading > PI) heading -= (2 * PI);
  else if (heading < -PI) heading += (2 * PI);

  // Convert everything from radians to degrees:
  heading *= 180.0 / PI;
  pitch *= 180.0 / PI;
  roll  *= 180.0 / PI;
  //bt.print("janky estimated angle is ");
  //Serial.println(gyro_angle);
  //Serial.print("Pitch, Roll: ");
  bt.print(roll, 2);
  bt.print(", ");
  bt.print(pitch, 2);
  bt.print(", ");
  bt.print(heading, 2);
  
  //bt.print(", ");
  
  //Serial.print("Heading: "); bt.println(heading, 2);
}

void print_matlab(){
  bt.print(millis()/1000);
  bt.print(",");
  bt.print(imu.calcAccel(imu.ax), 2);
  bt.print(", ");
  bt.print(imu.calcAccel(imu.ay), 2);
  bt.print(", ");
  bt.print(imu.calcAccel(imu.az), 2);
  bt.print(", ");
  bt.print(imu.calcGyro(imu.gx), 2);
  bt.print(", ");
  bt.print(imu.calcGyro(imu.gy), 2);
  bt.print(", ");
  bt.println(imu.calcGyro(imu.gz), 2);
}
void loop()
{
  // Update the sensor values whenever new data is available
  if ( imu.gyroAvailable() )
  {
    // To read from the gyroscope,  first call the
    // readGyro() function. When it exits, it'll update the
    // gx, gy, and gz variables with the most current data.
    imu.readGyro();
  }
  if ( imu.accelAvailable() )
  {
    // To read from the accelerometer, first call the
    // readAccel() function. When it exits, it'll update the
    // ax, ay, and az variables with the most current data.
    imu.readAccel();
  }
  if ( imu.magAvailable() )
  {
    // To read from the magnetometer, first call the
    // readMag() function. When it exits, it'll update the
    // mx, my, and mz variables with the most current data.
    imu.readMag();
  }

  if ((lastPrint + PRINT_SPEED) < millis())
  {
    //bt.println("The Program Started");
    //printGyro();  // Print "G: gx, gy, gz"
    //printAccel(); // Print "A: ax, ay, az"
    //printMag();   // Print "M: mx, my, mz"
    // Print the heading and orientation for fun!
    // Call print attitude. The LSM9DS1's mag x and y
    // axes are opposite to the accelerometer, so my, mx are
    // substituted for each other.
    printGyro();
    printAttitude(imu.ax, imu.ay, imu.az,
                 -imu.my, -imu.mx, imu.mz);
                 //printGyro();
                 bt.println();
    //print_matlab();
    //bt.println();
    lastPrint = millis(); // Update lastPrint time
    delay (5); //prepare for data (0.5s)

  }
  
}
