import UIKit
import Photos

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Kiểm tra quyền truy cập thư viện ảnh
        checkPhotoLibraryAuthorizationStatus()
        return true
    }

    private func checkPhotoLibraryAuthorizationStatus() {
        let status = PHPhotoLibrary.authorizationStatus()
        switch status {
        case .notDetermined:
            // Chưa được yêu cầu, yêu cầu quyền truy cập
            PHPhotoLibrary.requestAuthorization { status in
                if status == .authorized {
                    // Quyền đã được cấp
                    print("Photo library access granted.")
                } else {
                    // Quyền bị từ chối
                    print("Photo library access denied.")
                }
            }
        case .authorized:
            // Quyền đã được cấp
            print("Photo library access already granted.")
        case .restricted, .denied:
            // Quyền bị từ chối
            print("Photo library access denied.")
        @unknown default:
            break
        }
    }
}
