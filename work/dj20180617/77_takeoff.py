from dronekit import connect,VehicleMode
import time

# 機体に接続する​
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# アーミング可能かチェック
while not vehicle.is_armable:
    print "Waiting for vehicle to initialize..."
    time.sleep(1)


# アーミング実行​
# フライトモードを「GUIDED」に変更し、armedにTrueを設定する​
print "Arming motors"
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

# アーミングが完了するまで待機​
while not vehicle.armed and not vehicle.mode.name == 'GUIDED':
    print "Waiting for arming..."
    time.sleep(1)


# 目標高度を設定​
targetAltitude = 20

# テイクオフ実行​
# 20メートルの高さまで離陸する
print "Take off!!!"
vehicle.simple_takeoff(targetAltitude)

# 目標の高度に達するまで待つ​
while True:
    currentAltitude = vehicle.location.global_relative_frame.alt
    print "Altitude: ", currentAltitude

    if currentAltitude >= targetAltitude * 0.95:
        print "Reached target altitude (%s)" % targetAltitude
        break
    
    time.sleep(1)

print "lastAltitude: ", vehicle.location.global_relative_frame.alt