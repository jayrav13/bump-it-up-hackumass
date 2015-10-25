//
//  ViewController.swift
//  HackUMass
//
//  Created by Jay Ravaliya on 10/24/15.
//  Copyright © 2015 JRav. All rights reserved.
//

import UIKit
import CoreMotion
import CoreLocation
import Alamofire
import SwiftyJSON

extension NSDate {
    struct Date {
        static let formatter = NSDateFormatter()
    }
    var formatted: String {
        Date.formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SSSX"
        Date.formatter.timeZone = NSTimeZone(forSecondsFromGMT: 0)
        Date.formatter.calendar = NSCalendar(calendarIdentifier: NSCalendarIdentifierISO8601)!
        Date.formatter.locale = NSLocale(localeIdentifier: "en_US_POSIX")
        return Date.formatter.stringFromDate(self)
    }
}

class ViewController: UIViewController, CLLocationManagerDelegate {

    // set up motion and location managers
    var motionManager = CMMotionManager()
    var locationManager : CLLocationManager!

    // currLatLng is updated by the didUpdateLocations delegate method
    var currLatLng : [Double]!
    
    // final data stores the data to be pushed to server. arr stores current.
    var finalData : [[String : AnyObject]]!
    var arr : [String : AnyObject]!
    
    // button and boolean will toggle updating data
    var button : UIButton!
    var isUpdating : Bool!
    
    // screen height/width
    var screenWidth = UIScreen.mainScreen().bounds.width
    var screenHeight = UIScreen.mainScreen().bounds.height
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        button = UIButton(type: UIButtonType.System)
        button.frame = CGRect(x: 0, y: screenHeight/2 - 30, width: screenWidth, height: 60)
        button.addTarget(self, action: "updateData:", forControlEvents: UIControlEvents.TouchUpInside)
        button.setTitle("Gather Data", forState: UIControlState.Normal)
        isUpdating = false
        currLatLng = [0.0, 0.0]
        finalData = []
        
        self.view.addSubview(button)
        
        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestWhenInUseAuthorization()
        locationManager.startUpdatingLocation()
        
        if motionManager.accelerometerAvailable {
            
            // update button and boolean
            self.button.setTitle("End Updating Data", forState: UIControlState.Normal)
            
            let queue = NSOperationQueue()
            motionManager.startAccelerometerUpdatesToQueue(queue, withHandler: { (data, error) -> Void in
                
                if let data = data {
                    
                    self.arr = [
                        "acc_x" : data.acceleration.x,
                        "acc_y" : data.acceleration.y,
                        "acc_z" : data.acceleration.z,
                        "lat" : Double((self.locationManager.location?.coordinate.latitude)!),
                        "lng" : Double((self.locationManager.location?.coordinate.longitude)!),
                        "time": NSDate().formatted
                    ]
                    
                    self.finalData.append(self.arr)
                    
                }
            })
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func locationManager(manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        
        currLatLng = [Double((manager.location?.coordinate.latitude)!), Double((manager.location?.coordinate.longitude)!)]
    
    }
    
    func updateData(sender : UIButton) {
        // print(finalData)
        
        Alamofire.request(Method.POST, "http://45.79.187.92:5000/hackumass/api", parameters: ["data" : finalData], encoding: ParameterEncoding.JSON, headers: nil).responseJSON { (request, response, result) -> Void in
            
            if result.isSuccess == true {
                print("Yay!")
                
            }
            
        }
        
    }


}

