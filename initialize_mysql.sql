
-- ----------------------------
-- Table structure for sensor_data
-- ----------------------------
DROP TABLE IF EXISTS sensor_data;
DROP TABLE IF EXISTS confidance;

CREATE TABLE confidance (
    id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    animal_name VARCHAR(255) NOT NULL,
    confidance_ratio INT NOT NULL,
    sensor_data_id INT NOT NULL,
    FOREIGN KEY (sensor_data_id)
        REFERENCES sensor_data (id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);

CREATE TABLE sensor_data (
  id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  image_name VARCHAR(255) NOT NULL,
  detected_at VARCHAR(255) NOT NULL,
  created_at timestamp NULL DEFAULT NULL,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

