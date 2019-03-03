;; Auto-generated. Do not edit!


(when (boundp 'imu_visual::Num)
  (if (not (find-package "IMU_VISUAL"))
    (make-package "IMU_VISUAL"))
  (shadow 'Num (find-package "IMU_VISUAL")))
(unless (find-package "IMU_VISUAL::NUM")
  (make-package "IMU_VISUAL::NUM"))

(in-package "ROS")
;;//! \htmlinclude Num.msg.html


(defclass imu_visual::Num
  :super ros::object
  :slots (_first_name ))

(defmethod imu_visual::Num
  (:init
   (&key
    ((:first_name __first_name) "")
    )
   (send-super :init)
   (setq _first_name (string __first_name))
   self)
  (:first_name
   (&optional __first_name)
   (if __first_name (setq _first_name __first_name)) _first_name)
  (:serialization-length
   ()
   (+
    ;; string _first_name
    4 (length _first_name)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _first_name
       (write-long (length _first_name) s) (princ _first_name s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _first_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _first_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get imu_visual::Num :md5sum-) "80e8c9c65232d3c1560d7601e9eb9de8")
(setf (get imu_visual::Num :datatype-) "imu_visual/Num")
(setf (get imu_visual::Num :definition-)
      "string first_name

")



(provide :imu_visual/Num "80e8c9c65232d3c1560d7601e9eb9de8")


