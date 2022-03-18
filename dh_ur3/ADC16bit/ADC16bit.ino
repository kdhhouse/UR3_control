#include <ADS1X15.h>
#include <ros.h>
#include <std_msgs/Float32.h>


ros::NodeHandle  nh;
std_msgs::Float32 link1_msg;
std_msgs::Float32 link2_msg;
std_msgs::Float32 link3_msg;
std_msgs::Float32 link4_msg;
std_msgs::Float32 link5_msg;
std_msgs::Float32 link6_msg;

ros::Publisher pub_range1( "link_data1", &link1_msg);
ros::Publisher pub_range2( "link_data2", &link2_msg);
ros::Publisher pub_range3( "link_data3", &link3_msg);
ros::Publisher pub_range4( "link_data4", &link4_msg);
ros::Publisher pub_range5( "link_data5", &link5_msg);
ros::Publisher pub_range6( "link_data6", &link6_msg);



ADS1115 ADS_1(0x48);
ADS1115 ADS_2(0x49);
ADS1115 ADS_3(0x4A);



void setup() 
{
  Serial.begin(57600);
  nh.initNode();
  nh.advertise(pub_range1);
  nh.advertise(pub_range2);
  nh.advertise(pub_range3);
  nh.advertise(pub_range4);
  nh.advertise(pub_range5);
  nh.advertise(pub_range6);

  
  ADS_1.begin();
  ADS_1.setGain(1);
  ADS_2.begin();
  ADS_2.setGain(1);
  ADS_3.begin();
  ADS_3.setGain(1);

  

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

  link1_msg.data = volts_1_01*10000;
  link2_msg.data = volts_1_23*10000;
  link3_msg.data = volts_2_01*10000;
  link4_msg.data = volts_2_23*10000;
  link5_msg.data = volts_3_01*10000;
  link6_msg.data = volts_3_23*10000;

  pub_range1.publish(&link1_msg);
  pub_range2.publish(&link2_msg);
  pub_range3.publish(&link3_msg);
  pub_range4.publish(&link4_msg);
  pub_range5.publish(&link5_msg);
  pub_range6.publish(&link6_msg);

  nh.spinOnce();

  delay(100);
}
