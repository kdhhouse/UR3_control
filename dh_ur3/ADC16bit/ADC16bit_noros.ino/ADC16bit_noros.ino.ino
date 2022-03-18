#include <ADS1X15.h>


ADS1115 ADS_1(0x48);
ADS1115 ADS_2(0x49);
ADS1115 ADS_3(0x4A);



void setup() 
{
  Serial.begin(57600);
  Serial.println(__FILE__);

  ADS_1.begin();
  ADS_1.setGain(16);
  ADS_2.begin();
  ADS_2.setGain(16);
  ADS_3.begin();
  ADS_3.setGain(16);
}

void loop() 
{
  int16_t val_1_01 = ADS_1.readADC_Differential_0_1();  
  int16_t val_1_23 = ADS_1.readADC_Differential_2_3(); 
  float volts_1_01 = ADS_1.toVoltage(val_1_01); 
  float volts_1_23 = ADS_1.toVoltage(val_1_23); 

  int16_t val_2_01 = ADS_2.readADC_Differential_0_1();  
  int16_t val_2_23 = ADS_2.readADC_Differential_2_3(); 
  float volts_2_01 = ADS_2.toVoltage(val_2_01); 
  float volts_2_23 = ADS_2.toVoltage(val_2_23); 

  int16_t val_3_01 = ADS_3.readADC_Differential_0_1();  
  int16_t val_3_23 = ADS_3.readADC_Differential_2_3(); 
  float volts_3_01 = ADS_3.toVoltage(val_3_01); 
  float volts_3_23 = ADS_3.toVoltage(val_3_23); 

//  Serial.print("\tval_1_01: "); Serial.print(val_1_01); Serial.print("\t"); Serial.println(volts_1_01, 3);
//  Serial.print("\tval_1_23: "); Serial.print(val_1_23); Serial.print("\t"); Serial.println(volts_1_23, 3);
//  Serial.println();
//
//  Serial.print("\tval_2_01: "); Serial.print(val_2_01); Serial.print("\t"); Serial.println(volts_2_01, 3);
//  Serial.print("\tval_2_23: "); Serial.print(val_2_23); Serial.print("\t"); Serial.println(volts_2_23, 3);
//  Serial.println();
//
//  Serial.print("\tval_3_01: "); Serial.print(val_3_01); Serial.print("\t"); Serial.println(volts_3_01, 3);
//  Serial.print("\tval_3_23: "); Serial.print(val_3_23); Serial.print("\t"); Serial.println(volts_3_23, 3);
//  Serial.println();

  Serial.print(volts_1_01*10000, 3); Serial.print(", "); Serial.print(volts_1_23*10000, 3);
  Serial.print(", "); Serial.print(volts_2_01*10000, 3); Serial.print(", ");
  Serial.print(volts_2_23*10000, 3); Serial.print(", "); Serial.print(volts_3_01*10000, 3); Serial.print(", "); Serial.println(volts_3_23*10000, 3);

  delay(50);
}
