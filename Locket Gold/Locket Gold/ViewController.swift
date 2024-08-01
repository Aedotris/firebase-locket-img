import UIKit
import Photos

class ViewController: UIViewController, UIImagePickerControllerDelegate & UINavigationControllerDelegate, UITextFieldDelegate {

    // MARK: - UI Elements

    private let scrollView = UIScrollView()
    private let contentView = UIView()

    private let titleLabel = UILabel()
    private let descriptionLabel = UILabel()

    private let emailLabel = UILabel()
    private let emailTextField = UITextField()
    private let passwordLabel = UILabel()
    private let passwordTextField = UITextField()
    private let captionLabel = UILabel()
    private let captionTextField = UITextField()

    private let previewImageViewContainer = UIView()
    private let previewImageView = UIImageView()
    private let previewImageTapGesture = UITapGestureRecognizer()

    private let submitButton = UIButton(type: .system)

    private let loadingView = UIView()
    private let loadingIndicator = UIActivityIndicatorView(style: .large)

    private let notificationBanner = UIView()
    private let notificationLabel = UILabel()

    private let copyrightLabel = UILabel()


    private var selectedImage: UIImage?
    private var selectedImageName: String? // Tên file ảnh gốc


    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        animateUI()
    }


    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        return .portrait
    }

    // MARK: - thiết lập UI

    private func setupUI() {
        view.backgroundColor = .systemBackground

        setupScrollView()
        setupContentView()

        setupTitleLabel()
        setupDescriptionLabel()

        setupInputLabel(emailLabel, text: "Email")
        setupTextField(emailTextField, placeholder: "Enter your email", isSecure: false)
        setupInputLabel(passwordLabel, text: "Password")
        setupTextField(passwordTextField, placeholder: "Enter your password", isSecure: true)
        setupInputLabel(captionLabel, text: "Caption")
        setupTextField(captionTextField, placeholder: "Write a caption...", isSecure: false)

        setupPreviewImageViewContainer()
        setupPreviewImageView()
        setupPreviewImageTapGesture()

        setupSubmitButton()

        setupLoadingView()
        setupLoadingIndicator()

        setupNotificationBanner()
        setupButtonHoverEffect(for: submitButton)

        // Ẩn bàn phím khi chạm ngoài vùng input
        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(hideKeyboard))
        view.addGestureRecognizer(tapGesture)

        setupCopyrightLabel()

        setupConstraints()
    }

    private func setupScrollView() {
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(scrollView)
    }

    private func setupContentView() {
        contentView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.addSubview(contentView)
    }

    private func setupTitleLabel() {
        titleLabel.text = "💛 Share Your Moment !"
        titleLabel.font = UIFont.systemFont(ofSize: 32, weight: .bold)
        titleLabel.textColor = .label
        titleLabel.alpha = 0
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(titleLabel)
    }

    private func setupDescriptionLabel() {
        descriptionLabel.text = "Upload an image and share your thoughts with the world."
        descriptionLabel.font = UIFont.systemFont(ofSize: 16, weight: .regular)
        descriptionLabel.textColor = .secondaryLabel
        descriptionLabel.numberOfLines = 0
        descriptionLabel.alpha = 0
        descriptionLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(descriptionLabel)
    }

    private func setupInputLabel(_ label: UILabel, text: String) {
        label.text = text
        label.font = UIFont.systemFont(ofSize: 14, weight: .medium)
        label.textColor = .label
        label.alpha = 0
        label.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(label)
    }

    private func setupTextField(_ textField: UITextField, placeholder: String, isSecure: Bool) {
        textField.attributedPlaceholder = NSAttributedString(
            string: placeholder,
            attributes: [NSAttributedString.Key.foregroundColor: UIColor.placeholderText]
        )
        textField.isSecureTextEntry = isSecure
        textField.borderStyle = .roundedRect
        textField.backgroundColor = UIColor(white: 0.95, alpha: 1)
        textField.layer.cornerRadius = 8
        textField.font = UIFont.systemFont(ofSize: 16)
        textField.alpha = 0
        textField.textColor = .black
        textField.translatesAutoresizingMaskIntoConstraints = false
        textField.heightAnchor.constraint(equalToConstant: 50).isActive = true
        textField.addPadding(left: 16)
        textField.delegate = self
        contentView.addSubview(textField)
    }

    private func setupPreviewImageViewContainer() {
        previewImageViewContainer.backgroundColor = UIColor(white: 0.95, alpha: 1)
        previewImageViewContainer.layer.cornerRadius = 8
        previewImageViewContainer.alpha = 0
        previewImageViewContainer.translatesAutoresizingMaskIntoConstraints = false
        previewImageViewContainer.heightAnchor.constraint(equalToConstant: 200).isActive = true
        contentView.addSubview(previewImageViewContainer)
    }

    private func setupPreviewImageView() {
        previewImageView.contentMode = .scaleAspectFill // Thay đổi contentMode
        previewImageView.clipsToBounds = true // Đảm bảo ảnh không tràn ra ngoài
        previewImageView.image = UIImage(systemName: "photo")?.withTintColor(.systemGray3, renderingMode: .alwaysOriginal)
        previewImageView.translatesAutoresizingMaskIntoConstraints = false
        previewImageViewContainer.addSubview(previewImageView)
        NSLayoutConstraint.activate([
            previewImageView.centerXAnchor.constraint(equalTo: previewImageViewContainer.centerXAnchor),
            previewImageView.centerYAnchor.constraint(equalTo: previewImageViewContainer.centerYAnchor),
            previewImageView.widthAnchor.constraint(equalTo: previewImageViewContainer.widthAnchor), // Giữ nguyên chiều rộng
            previewImageView.heightAnchor.constraint(equalTo: previewImageViewContainer.heightAnchor) // Giữ nguyên chiều cao
        ])
    }

    private func setupPreviewImageTapGesture() {
        previewImageTapGesture.addTarget(self, action: #selector(handlePreviewImageTap))
        previewImageViewContainer.addGestureRecognizer(previewImageTapGesture)
    }

    private func setupSubmitButton() {
        submitButton.setTitle("Submit 💛", for: .normal)
        submitButton.setTitleColor(.black, for: .normal)
        submitButton.backgroundColor = .white
        submitButton.layer.cornerRadius = 8
        submitButton.titleLabel?.font = UIFont.systemFont(ofSize: 18, weight: .medium)
        submitButton.addTarget(self, action: #selector(submitForm), for: .touchUpInside)
        submitButton.alpha = 0
        submitButton.translatesAutoresizingMaskIntoConstraints = false
        submitButton.heightAnchor.constraint(equalToConstant: 50).isActive = true
        contentView.addSubview(submitButton)
    }

    private func setupLoadingView() {
        loadingView.backgroundColor = UIColor.black.withAlphaComponent(0.6)
        loadingView.isHidden = true
        loadingView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(loadingView)
        NSLayoutConstraint.activate([
            loadingView.topAnchor.constraint(equalTo: view.topAnchor),
            loadingView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            loadingView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            loadingView.trailingAnchor.constraint(equalTo: view.trailingAnchor)
        ])
    }

    private func setupLoadingIndicator() {
        loadingIndicator.color = .white
        loadingIndicator.hidesWhenStopped = true
        loadingIndicator.translatesAutoresizingMaskIntoConstraints = false
        loadingView.addSubview(loadingIndicator)
        NSLayoutConstraint.activate([
            loadingIndicator.centerXAnchor.constraint(equalTo: loadingView.centerXAnchor),
            loadingIndicator.centerYAnchor.constraint(equalTo: loadingView.centerYAnchor)
        ])
    }

    private func setupNotificationBanner() {
        notificationBanner.backgroundColor = UIColor.green.withAlphaComponent(0.8)
        notificationBanner.isHidden = true
        notificationBanner.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(notificationBanner)

        notificationLabel.textColor = .white
        notificationLabel.font = UIFont.systemFont(ofSize: 16, weight: .medium)
        notificationLabel.textAlignment = .center
        notificationLabel.numberOfLines = 0
        notificationLabel.translatesAutoresizingMaskIntoConstraints = false
        notificationBanner.addSubview(notificationLabel)

        NSLayoutConstraint.activate([
            notificationBanner.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -64),
            notificationBanner.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 24),
            notificationBanner.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -24),
            notificationBanner.heightAnchor.constraint(equalToConstant: 64),

            notificationLabel.centerYAnchor.constraint(equalTo: notificationBanner.centerYAnchor),
            notificationLabel.leadingAnchor.constraint(equalTo: notificationBanner.leadingAnchor, constant: 16),
            notificationLabel.trailingAnchor.constraint(equalTo: notificationBanner.trailingAnchor, constant: -16)
        ])
    }

    private func setupCopyrightLabel() {
        copyrightLabel.text = "© Lê Vinh Khang 2024"
        copyrightLabel.font = UIFont.systemFont(ofSize: 12, weight: .light)
        copyrightLabel.textColor = .secondaryLabel
        copyrightLabel.textAlignment = .center
        copyrightLabel.alpha = 0
        copyrightLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(copyrightLabel)
    }


    private func setupConstraints() {
        NSLayoutConstraint.activate([
            scrollView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            scrollView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
            scrollView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            scrollView.trailingAnchor.constraint(equalTo: view.trailingAnchor),

            contentView.topAnchor.constraint(equalTo: scrollView.topAnchor),
            contentView.bottomAnchor.constraint(equalTo: scrollView.bottomAnchor),
            contentView.leadingAnchor.constraint(equalTo: scrollView.leadingAnchor),
            contentView.trailingAnchor.constraint(equalTo: scrollView.trailingAnchor),
            contentView.widthAnchor.constraint(equalTo: view.widthAnchor),

            titleLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 32),
            titleLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 24),
            titleLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -24),

            descriptionLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 8),
            descriptionLabel.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),
            descriptionLabel.trailingAnchor.constraint(equalTo: titleLabel.trailingAnchor),

            emailLabel.topAnchor.constraint(equalTo: descriptionLabel.bottomAnchor, constant: 32),
            emailLabel.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),

            emailTextField.topAnchor.constraint(equalTo: emailLabel.bottomAnchor, constant: 8),
            emailTextField.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),
            emailTextField.trailingAnchor.constraint(equalTo: titleLabel.trailingAnchor),

            passwordLabel.topAnchor.constraint(equalTo: emailTextField.bottomAnchor, constant: 16),
            passwordLabel.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),

            passwordTextField.topAnchor.constraint(equalTo: passwordLabel.bottomAnchor, constant: 8),
            passwordTextField.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),
            passwordTextField.trailingAnchor.constraint(equalTo: titleLabel.trailingAnchor),

            captionLabel.topAnchor.constraint(equalTo: passwordTextField.bottomAnchor, constant: 16),
            captionLabel.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),

            captionTextField.topAnchor.constraint(equalTo: captionLabel.bottomAnchor, constant: 8),
            captionTextField.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),
            captionTextField.trailingAnchor.constraint(equalTo: titleLabel.trailingAnchor),

            previewImageViewContainer.topAnchor.constraint(equalTo: captionTextField.bottomAnchor, constant: 32),
            previewImageViewContainer.leadingAnchor.constraint(equalTo: captionTextField.leadingAnchor),
            previewImageViewContainer.trailingAnchor.constraint(equalTo: captionTextField.trailingAnchor),

            submitButton.topAnchor.constraint(equalTo: previewImageViewContainer.bottomAnchor, constant: 32),
            submitButton.leadingAnchor.constraint(equalTo: previewImageViewContainer.leadingAnchor),
            submitButton.trailingAnchor.constraint(equalTo: previewImageViewContainer.trailingAnchor),
            submitButton.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -32),

            copyrightLabel.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -8),
            copyrightLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }

    private func animateUI() {
        let elements = [titleLabel, descriptionLabel, emailLabel, emailTextField, passwordLabel, passwordTextField, captionLabel, captionTextField, previewImageViewContainer, submitButton]
        for (index, element) in elements.enumerated() {
            UIView.animate(withDuration: 0.8, delay: Double(index) * 0.1, usingSpringWithDamping: 0.7, initialSpringVelocity: 0.5, options: .curveEaseInOut) {
                element.alpha = 1
                element.transform = CGAffineTransform(translationX: 0, y: -20)
            }
        }

        UIView.animate(withDuration: 0.8, delay: 1.0, usingSpringWithDamping: 0.7, initialSpringVelocity: 0.5, options: .curveEaseInOut) {
            self.copyrightLabel.alpha = 1
            self.copyrightLabel.transform = CGAffineTransform(translationX: 0, y: -20)
        }
    }

    // MARK: - Hành Động

    @objc private func handlePreviewImageTap() {
        let status = PHPhotoLibrary.authorizationStatus()
        if status == .authorized {
            openImagePicker()
        } else {
            PHPhotoLibrary.requestAuthorization { status in
                if status == .authorized {
                    DispatchQueue.main.async {
                        self.openImagePicker()
                    }
                } else {
                    DispatchQueue.main.async {
                        self.showAccessDeniedAlert()
                    }
                }
            }
        }
    }

    private func openImagePicker() {
        let picker = UIImagePickerController()
        picker.delegate = self
        picker.sourceType = .photoLibrary
        present(picker, animated: true, completion: nil)
    }

    private func showAccessDeniedAlert() {
        let alert = UIAlertController(
            title: "Access Denied",
            message: "Please grant access to your photo library in Settings to select an image.",
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert, animated: true, completion: nil)
    }

    @objc private func submitForm() {
        guard let image = selectedImage,
              let email = emailTextField.text, !email.isEmpty,
              let password = passwordTextField.text, !password.isEmpty,
              let caption = captionTextField.text, !caption.isEmpty else {
            showAlert(title: "Error", message: "Please fill in all fields and select an image.")
            return
        }
        uploadImage(image: image, email: email, password: password, caption: caption)
    }

    // MARK: - Tải ảnh

    private func uploadImage(image: UIImage, email: String, password: String, caption: String) {
        loadingView.isHidden = false
        loadingIndicator.startAnimating()
        
        let url = URL(string: "https://locket-three.vercel.app/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        let imageData = image.jpegData(compressionQuality: 0.8)
        
        if let imageData = imageData, let fileName = selectedImageName {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileName)\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
            body.append(imageData)
            body.append("\r\n".data(using: .utf8)!)
        }
        
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"email\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(email)\r\n".data(using: .utf8)!)
        
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"password\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(password)\r\n".data(using: .utf8)!)
        
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"caption\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(caption)\r\n".data(using: .utf8)!)
        
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        let task = URLSession.shared.uploadTask(with: request, from: body) { data, response, error in
            DispatchQueue.main.async {
                self.loadingView.isHidden = true
                self.loadingIndicator.stopAnimating()
            }
            
            if let error = error {
                print("Lỗi khi upload: \(error)")
                self.showAlert(title: "Upload Failed", message: error.localizedDescription)
                return
            }
            
            if let response = response as? HTTPURLResponse {
                switch response.statusCode {
                case 200:
                    print("Upload thành công!")
                    self.showAlert(title: "Success", message: "Image uploaded successfully!")
                case 500:
                    print("Upload thất bại.")
                    self.showAlert(title: "Upload Failed", message: "Image upload failed. Please try again.")
                default:
                    print("Status code khác: \(response.statusCode)")
                    self.showAlert(title: "Upload Failed", message: "An error occurred. Please try again.")
                }
            }
        }
        
        task.resume()
    }


    // MARK: - Helpers

    private func showAlert(title: String, message: String) {
        DispatchQueue.main.async { // Hiển thị alert trên main thread
            let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
            self.present(alert, animated: true, completion: nil)
        }
    }

    private func showNotification(message: String, isSuccess: Bool) {
        DispatchQueue.main.async {
            self.notificationLabel.text = message
            self.notificationBanner.backgroundColor = isSuccess ? UIColor.green.withAlphaComponent(0.8) : UIColor.red.withAlphaComponent(0.8)
            self.notificationBanner.isHidden = false

            UIView.animate(withDuration: 0.5, delay: 0, usingSpringWithDamping: 0.7, initialSpringVelocity: 0.5, options: .curveEaseInOut) {
                self.notificationBanner.transform = .identity
            } completion: { _ in
                UIView.animate(withDuration: 0.5, delay: 2.0, usingSpringWithDamping: 0.7, initialSpringVelocity: 0.5, options: .curveEaseInOut) {
                    self.notificationBanner.transform = CGAffineTransform(translationX: 0, y: 80)
                } completion: { _ in
                    self.notificationBanner.isHidden = true
                }
            }
        }
    }

    private func setupButtonHoverEffect(for button: UIButton) {
        button.addTarget(self, action: #selector(buttonTouchDown(_:)), for: .touchDown)
        button.addTarget(self, action: #selector(buttonTouchUp(_:)), for: [.touchUpInside, .touchUpOutside, .touchCancel])
    }

    @objc private func buttonTouchDown(_ button: UIButton) {
        UIView.animate(withDuration: 0.1, delay: 0, options: [.allowUserInteraction, .curveEaseInOut], animations: {
            button.transform = CGAffineTransform(scaleX: 0.95, y: 0.95)
        }, completion: nil)
    }

    @objc private func buttonTouchUp(_ button: UIButton) {
        UIView.animate(withDuration: 0.3, delay: 0, usingSpringWithDamping: 0.5, initialSpringVelocity: 3, options: [.allowUserInteraction, .curveEaseInOut], animations: {
            button.transform = .identity
        }, completion: nil)
    }

    // MARK: - Ẩn bàn phím

    @objc private func hideKeyboard() {
        view.endEditing(true)
    }


    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }


    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]) {
        picker.dismiss(animated: true, completion: nil)
        if let image = info[.originalImage] as? UIImage, let asset = info[.phAsset] as? PHAsset {
            selectedImage = image
            previewImageView.image = image
            previewImageView.contentMode = .scaleAspectFill

            // Lấy tên file ảnh gốc
            if let fileName = asset.value(forKey: "filename") as? String {
                selectedImageName = fileName
            }
        }
    }

    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true, completion: nil)
    }
}


extension UITextField {
    func addPadding(left: CGFloat) {
        let paddingView = UIView(frame: CGRect(x: 0, y: 0, width: left, height: self.frame.height))
        self.leftView = paddingView
        self.leftViewMode = .always
    }
}
