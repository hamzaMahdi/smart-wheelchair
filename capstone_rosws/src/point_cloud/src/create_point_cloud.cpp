#include "ros/ros.h"
#include "tf/transform_listener.h"
#include "sensor_msgs/PointCloud.h"
#include "tf/message_filter.h"
#include "message_filters/subscriber.h"
#include "laser_geometry/laser_geometry.h"

class LaserScanToPointCloud{

public:

  ros::NodeHandle n_;
  laser_geometry::LaserProjection projector_;
  tf::TransformListener listener_;
  //message_filters::Subscriber<sensor_msgs::LaserScan> laser_sub_;
  //tf::MessageFilter<sensor_msgs::LaserScan> laser_notifier_;
  ros::Publisher scan_pub_;
  ros::Subscriber scan_sub_;

  LaserScanToPointCloud(ros::NodeHandle n)//: 
    //n_(n),
    //laser_sub_(n_, "base_scan", 10),
    //laser_notifier_("scan",listener_, "base_link", 10)
  {
    //laser_notifier_.registerCallback(
      //boost::bind(&LaserScanToPointCloud::scanCallback, this, _1));
    //laser_notifier_.setTolerance(ros::Duration(0.01));
    scan_pub_ = n_.advertise<sensor_msgs::PointCloud>("/my_cloud",1);
    scan_sub_ = n_.subscribe<sensor_msgs::LaserScan>("scan", 10, &LaserScanToPointCloud::scanCallback, this);
  }

  void scanCallback (const sensor_msgs::LaserScan::ConstPtr& scan_in)
  {
    sensor_msgs::PointCloud cloud;
    try
    {
        projector_.projectLaser(
          *scan_in, cloud);
    }
    catch (tf::TransformException& e)
    {
        std::cout << e.what();
        return;
    }
    
    // Do something with cloud.

    scan_pub_.publish(cloud);

  }
};

int main(int argc, char** argv)
{
  
  ros::init(argc, argv, "my_scan_to_cloud");
  ros::NodeHandle n;
  LaserScanToPointCloud lstopc(n);
  
  ros::spin();
  
  return 0;
}
