////////////////////////////////////////////////////////////////////////////
//
//  This file is part of RTIMULib-Arduino
//
//  Copyright (c) 2014-2015, richards-tech
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy of
//  this software and associated documentation files (the "Software"), to deal in
//  the Software without restriction, including without limitation the rights to use,
//  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
//  Software, and to permit persons to whom the Software is furnished to do so,
//  subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
//  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
//  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
//  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
//  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
//  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include "RTIMULSM9DS1.h"
#include "RTIMUSettings.h"

#if defined(LSM9DS1_73) 


RTIMULSM9DS1::RTIMULSM9DS1(RTIMUSettings *settings) : RTIMU(settings)
{
    m_sampleRate = 100;
}

RTIMULSM9DS1::~RTIMULSM9DS1()
{
}

int RTIMULSM9DS1::IMUInit()
{
    unsigned char result;

    //  configure IMU

   m_accelGyroSlaveAddr = m_settings->m_I2CSlaveAddress;
   /*
    if (m_accelGyroSlaveAddr == LSM9DS1_ADDRESS0)
        m_magSlaveAddr= LSM9DS1_MAG_ADDRESS0;
    else if ()
        m_magSlaveAddr = LSM9DS1_MAG_ADDRESS1;
*/
    if (I2Cdev::readByte(LSM9DS1_MAG_ADDRESS0, LSM9DS1_MAG_WHO_AM_I, &result)) {
        if (result == LSM9DS1_MAG_ID) {
            m_magSlaveAddr = LSM9DS1_MAG_ADDRESS0;
        }
    } else if (I2Cdev::readByte(LSM9DS1_MAG_ADDRESS1, LSM9DS1_MAG_WHO_AM_I, &result)) {
        if (result == LSM9DS1_MAG_ID) {
            m_magSlaveAddr = LSM9DS1_MAG_ADDRESS1;
        }
    } else if (I2Cdev::readByte(LSM9DS1_MAG_ADDRESS2, LSM9DS1_MAG_WHO_AM_I,&result)) {
        if (result == LSM9DS1_MAG_ID) {
            m_magSlaveAddr = LSM9DS1_MAG_ADDRESS2;
        }
    } else if (I2Cdev::readByte(LSM9DS1_MAG_ADDRESS3, LSM9DS1_MAG_WHO_AM_I, &result)) {
        if (result == LSM9DS1_MAG_ID) {
            m_magSlaveAddr = LSM9DS1_MAG_ADDRESS3;
        }
    }
    setCalibrationData();

    //  Set up the gyro

    if (!I2Cdev::writeByte(m_accelGyroSlaveAddr, LSM9DS1_CTRL8, 0x80))
        return -1;
        delay(100);

    if (!I2Cdev::readByte(m_accelGyroSlaveAddr, LSM9DS1_WHO_AM_I, &result))
        return -2;

    if (result != LSM9DS1_ID) {
        //Serial.println(LSM9DS1_ID);
        //Serial.println(result);
        Serial.println(m_accelGyroSlaveAddr);
        return -3;
    }

    if (!setGyroSampleRate())
            return -4;

    if (!setGyroCTRL3())
            return -5;

    //if (!setGyroCTRL4())
      //      return -6;

    //  Set up the accel

    if (!I2Cdev::readByte(m_magSlaveAddr, LSM9DS1_MAG_WHO_AM_I, &result))
        return -7;

    if (result != LSM9DS1_MAG_ID) {
        return -8;
    }

    if (!setAccelCTRL6())
        return 9;

    if (!setAccelCTRL7())
        return -10;

    if (!setCompassCTRL1())
        return 11;

    if (!setCompassCTRL2())
        return -12;

    if (!setCompassCTRL3())
        return -13;

    //if (!setGyroCTRL5())
      //      return -14;

    gyroBiasInit();
    return 1;
}

bool RTIMULSM9DS1::setGyroSampleRate()
{
    unsigned char ctrl1;

    switch (m_settings->m_LSM9DS1GyroSampleRate) {
    case LSM9DS1_GYRO_SAMPLERATE_14_9:
        ctrl1 = 0x20;
        m_sampleRate = 15;
        break;

    case LSM9DS1_GYRO_SAMPLERATE_59_5:
        ctrl1 = 0x40;
        m_sampleRate = 60;
        break;

    case LSM9DS1_GYRO_SAMPLERATE_119:
        ctrl1 = 0x60;
        m_sampleRate = 119;
        break;

    case LSM9DS1_GYRO_SAMPLERATE_238:
        ctrl1 = 0x80;
        m_sampleRate = 238;
        break;

    case LSM9DS1_GYRO_SAMPLERATE_476:
        ctrl1 = 0xa0;
        m_sampleRate = 476;
        break;

    case LSM9DS1_GYRO_SAMPLERATE_952:
        ctrl1 = 0xc0;
        m_sampleRate = 952;
        break;

    default:
        return false;
    }


    m_sampleInterval = (uint64_t)1000000 / m_sampleRate;

   switch (m_settings->m_LSM9DS1GyroBW) {
    case LSM9DS1_GYRO_BANDWIDTH_0:
        ctrl1 |= 0x00;
        break;

    case LSM9DS1_GYRO_BANDWIDTH_1:
        ctrl1 |= 0x01;
        break;

    case LSM9DS1_GYRO_BANDWIDTH_2:
        ctrl1 |= 0x02;
        break;

    case LSM9DS1_GYRO_BANDWIDTH_3:
        ctrl1 |= 0x03;
        break;
    }

    switch (m_settings->m_LSM9DS1GyroFsr) {
    case LSM9DS1_GYRO_FSR_250:
        ctrl1 |= 0x00;
        m_gyroScale = (RTFLOAT)0.00875 * RTMATH_DEGREE_TO_RAD;
        break;

    case LSM9DS1_GYRO_FSR_500:
        ctrl1 |= 0x08;
        m_gyroScale = (RTFLOAT)0.0175 * RTMATH_DEGREE_TO_RAD;
        break;

    case LSM9DS1_GYRO_FSR_2000:
        ctrl1 |= 0x18;
        m_gyroScale = (RTFLOAT)0.07 * RTMATH_DEGREE_TO_RAD;
        break;

    default:
        return false;
    }
    return (I2Cdev::writeByte(m_accelGyroSlaveAddr, LSM9DS1_CTRL1, ctrl1));
}

bool RTIMULSM9DS1::setGyroCTRL3()
{
    unsigned char ctrl3;

    if ((m_settings->m_LSM9DS1GyroHpf < LSM9DS1_GYRO_HPF_0) || (m_settings->m_LSM9DS1GyroHpf > LSM9DS1_GYRO_HPF_9)) {
        return false;
    }
       ctrl3 = m_settings->m_LSM9DS1GyroHpf;

    //  Turn on hpf
    ctrl3 |= 0x40;
    return I2Cdev::writeByte(m_accelGyroSlaveAddr,  LSM9DS1_CTRL3, ctrl3);
}

bool RTIMULSM9DS1::setAccelCTRL6()
{
       unsigned char ctrl6;

    if ((m_settings->m_LSM9DS1AccelSampleRate < 0) || (m_settings->m_LSM9DS1AccelSampleRate > 6)) {
        return false;
    }

    ctrl6 = (m_settings->m_LSM9DS1AccelSampleRate << 5);

    if ((m_settings->m_LSM9DS1AccelLpf < 0) || (m_settings->m_LSM9DS1AccelLpf > 3)) {
        return false;
    }

    switch (m_settings->m_LSM9DS1AccelFsr) {
    case LSM9DS1_ACCEL_FSR_2:
        m_accelScale = (RTFLOAT)0.000061;
        break;

    case LSM9DS1_ACCEL_FSR_4:
        m_accelScale = (RTFLOAT)0.000122;
        break;

    case LSM9DS1_ACCEL_FSR_8:
        m_accelScale = (RTFLOAT)0.000244;
        break;

    case LSM9DS1_ACCEL_FSR_16:
        m_accelScale = (RTFLOAT)0.000732;
        break;

    default:
        return false;
    }

    ctrl6 |= (m_settings->m_LSM9DS1AccelLpf) | (m_settings->m_LSM9DS1AccelFsr << 3);


    return I2Cdev::writeByte(m_accelGyroSlaveAddr,  LSM9DS1_CTRL6, ctrl6);
}

bool RTIMULSM9DS1::setAccelCTRL7()
{
    unsigned char ctrl7;

    ctrl7 = 0x00;
    //Bug: Bad things happen.
    //ctrl7 = 0x05;

    return I2Cdev::writeByte(m_accelGyroSlaveAddr,  LSM9DS1_CTRL7, ctrl7);
}


bool RTIMULSM9DS1::setCompassCTRL1()
{
     unsigned char ctrl1;

    if ((m_settings->m_LSM9DS1CompassSampleRate < 0) || (m_settings->m_LSM9DS1CompassSampleRate > 5)) {
        return false;
    }

    ctrl1 = (m_settings->m_LSM9DS1CompassSampleRate << 2);

    return I2Cdev::writeByte(m_magSlaveAddr,  LSM9DS1_MAG_CTRL1, ctrl1);
}

bool RTIMULSM9DS1::setCompassCTRL2()
{
       unsigned char ctrl2;

    //  convert FSR to uT

    switch (m_settings->m_LSM9DS1CompassFsr) {
    case LSM9DS1_COMPASS_FSR_4:
        ctrl2 = 0;
        m_compassScale = (RTFLOAT)0.014;
        break;

    case LSM9DS1_COMPASS_FSR_8:
        ctrl2 = 0x20;
        m_compassScale = (RTFLOAT)0.029;
        break;

    case LSM9DS1_COMPASS_FSR_12:
        ctrl2 = 0x40;
        m_compassScale = (RTFLOAT)0.043;
        break;

    case LSM9DS1_COMPASS_FSR_16:
        ctrl2 = 0x60;
        m_compassScale = (RTFLOAT)0.058;
        break;

    default:
        return false;
    }

    return I2Cdev::writeByte(m_magSlaveAddr,  LSM9DS1_MAG_CTRL2, ctrl2);
}

bool RTIMULSM9DS1::setCompassCTRL3()
{
     return I2Cdev::writeByte(m_magSlaveAddr,  LSM9DS1_MAG_CTRL3, 0x00);
}

int RTIMULSM9DS1::IMUGetPollInterval()
{
    return (400 / m_sampleRate);
}

bool RTIMULSM9DS1::IMURead()
{
    unsigned char status;
    unsigned char gyroData[6];
    unsigned char accelData[6];
    unsigned char compassData[6];

    if (!I2Cdev::readByte(m_accelGyroSlaveAddr, LSM9DS1_STATUS, &status))
        return false;

    if ((status & 0x3) == 0)
        return false;

    for (int i = 0; i<6; i++){
        if (!I2Cdev::readBytes(m_accelGyroSlaveAddr, LSM9DS1_OUT_X_L_G + i, 1, &gyroData[i]))
            return false;

        if (!I2Cdev::readBytes(m_accelGyroSlaveAddr, LSM9DS1_OUT_X_L_XL + i, 1, &accelData[i]))
            return false;

        if (!I2Cdev::readBytes(m_magSlaveAddr, LSM9DS1_MAG_OUT_X_L + i, 1, &compassData[i]))
            return false;
    }

    m_timestamp = millis();

    RTMath::convertToVector(gyroData, m_gyro, m_gyroScale, false);
    RTMath::convertToVector(accelData, m_accel, m_accelScale, false);
    RTMath::convertToVector(compassData, m_compass, m_compassScale, false);

    //  sort out gyro axes

    m_gyro.setZ(-m_gyro.z());


    //  sort out accel data;

    m_accel.setX(-m_accel.x());
    m_accel.setY(-m_accel.y());

    //  sort out compass axes

    m_compass.setX(-m_compass.x());
    m_compass.setZ(-m_compass.z());

    //  now do standard processing

    handleGyroBias();
    calibrateAverageCompass();

    return true;
}
#endif
