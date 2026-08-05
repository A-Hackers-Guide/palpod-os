import Foundation
#if canImport(AVFoundation) && canImport(UIKit)
import AVFoundation
import SwiftUI
import UIKit

/// SwiftUI wrapper around AVCaptureSession for scanning the pairing QR.
/// Emits parsed `hearth://pair?token=...&fingerprint=...` URLs upstream.
public struct QRScanner: UIViewControllerRepresentable {
    public var onCode: (URL) -> Void

    public init(onCode: @escaping (URL) -> Void) { self.onCode = onCode }

    public func makeUIViewController(context: Context) -> QRScannerVC {
        let vc = QRScannerVC()
        vc.onCode = onCode
        return vc
    }
    public func updateUIViewController(_ vc: QRScannerVC, context: Context) {}
}

public final class QRScannerVC: UIViewController, AVCaptureMetadataOutputObjectsDelegate {
    var onCode: ((URL) -> Void)?
    private let session = AVCaptureSession()
    private var preview: AVCaptureVideoPreviewLayer?

    public override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .black
        setupCapture()
    }

    public override func viewWillLayoutSubviews() {
        super.viewWillLayoutSubviews()
        preview?.frame = view.bounds
    }

    public override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        if !session.isRunning { session.startRunning() }
    }

    public override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        if session.isRunning { session.stopRunning() }
    }

    private func setupCapture() {
        guard let device = AVCaptureDevice.default(for: .video),
              let input = try? AVCaptureDeviceInput(device: device) else { return }
        if session.canAddInput(input) { session.addInput(input) }
        let output = AVCaptureMetadataOutput()
        if session.canAddOutput(output) {
            session.addOutput(output)
            output.setMetadataObjectsDelegate(self, queue: .main)
            output.metadataObjectTypes = [.qr]
        }
        let p = AVCaptureVideoPreviewLayer(session: session)
        p.videoGravity = .resizeAspectFill
        view.layer.addSublayer(p)
        preview = p
    }

    public func metadataOutput(_ output: AVCaptureMetadataOutput,
                               didOutput metadataObjects: [AVMetadataObject],
                               from connection: AVCaptureConnection) {
        guard let obj = metadataObjects.first as? AVMetadataMachineReadableCodeObject,
              let raw = obj.stringValue,
              let url = URL(string: raw),
              url.scheme == "hearth",
              url.host == "pair" else { return }
        session.stopRunning()
        onCode?(url)
    }
}
#endif

/// Parsed `hearth://pair?token=...&fingerprint=...` payload.
public struct PairPayload: Equatable, Sendable {
    public let token: String
    public let fingerprint: String

    /// Returns nil if the URL is not a valid pair link.
    public init?(url: URL) {
        guard url.scheme == "hearth", url.host == "pair" else { return nil }
        guard let comps = URLComponents(url: url, resolvingAgainstBaseURL: false),
              let items = comps.queryItems else { return nil }
        var token: String?
        var fingerprint: String?
        for i in items {
            switch i.name {
            case "token":       token = i.value
            case "fingerprint": fingerprint = i.value
            default: break
            }
        }
        guard let t = token, let fp = fingerprint else { return nil }
        self.token = t
        self.fingerprint = fp
    }
}
