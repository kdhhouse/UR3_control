#include <ros.h>
#include <std_msgs/Float32MultiArray.h>

ros::NodeHandle  nh;
std_msgs::Float32MultiArray range_msg;
ros::Publisher pub_range( "range_data", &range_msg);


const int analog_pin1 = 5;
const int analog_pin2 = 4;

/*
 * getRange() - samples the analog input from the ranger
 * and converts it into meters.  
 * 
 * NOTE: This function is only applicable to the GP2D120XJ00F !!
 * Using this function with other Rangers will provide incorrect readings.
 */
float getRange(int pin_num){
    float sample;
    // Get data
    sample = analogRead(pin_num);
    return sample;
}

void setup()
{
  nh.initNode();
  nh.advertise(pub_range);
  range_msg.data = (float*)malloc(sizeof(float) * 2);
  range_msg.data_length = 2;
  
}

void loop()
{
  range_msg.data[0] = getRange(analog_pin1)*200/1024;
  range_msg.data[1] = getRange(analog_pin2)*200/1024;
  pub_range.publish(&range_msg);

  nh.spinOnce();
  delay(1000);
}
